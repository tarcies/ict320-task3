"""Pages, access control and form handling, using Flask's test client."""

import pytest

from app.services import summary_service, survey_service
from app.utils.errors import DuplicateSummary, NoSurveysForDate
from tests.conftest import NEW_DAY, stock

PAGES = ["/", "/surveys/", "/surveys/new", "/equipment/", "/summaries/"]


# ---------- access control ----------


@pytest.mark.parametrize("path", PAGES)
def test_anonymous_visitors_are_sent_to_login(client, path):
    response = client.get(path)
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_login_page_is_public(client):
    assert client.get("/login").status_code == 200


def test_wrong_password_is_rejected(client, monkeypatch):
    monkeypatch.setattr("app.routes.auth.authenticate", lambda u, p: None)
    response = client.post("/login", data={"username": "x", "password": "y"})
    assert response.status_code == 401
    assert b"Invalid username or password" in response.data


def test_correct_login_starts_a_session(client, monkeypatch):
    user = {"id": 1, "username": "mia", "role": "field"}
    monkeypatch.setattr("app.routes.auth.authenticate", lambda u, p: user)
    response = client.post("/login", data={"username": "mia", "password": "pw"})
    assert response.status_code == 302
    with client.session_transaction() as s:
        assert s["user"]["username"] == "mia"


def test_logout_clears_the_session(field):
    assert field.get("/logout").status_code == 302
    assert "/login" in field.get("/").headers["Location"]


def test_field_user_cannot_generate_summaries(field):
    response = field.post("/summaries/generate", data={"date": "2026-10-06"})
    assert response.status_code == 403


def test_generate_form_is_hidden_from_field_users(field, monkeypatch):
    monkeypatch.setattr(summary_service, "get_all_summaries", lambda: [])
    assert b"/summaries/generate" not in field.get("/summaries/").data


def test_generate_form_is_shown_to_admins(admin, monkeypatch):
    monkeypatch.setattr(summary_service, "get_all_summaries", lambda: [])
    assert b"/summaries/generate" in admin.get("/summaries/").data


# ---------- pages render ----------


@pytest.mark.parametrize("path", ["/", "/surveys/", "/surveys/new", "/equipment/"])
def test_pages_render_for_signed_in_users(mongo, monkeypatch, field, path):
    monkeypatch.setattr(summary_service, "get_all_summaries", lambda: [])
    assert field.get(path).status_code == 200


def test_survey_list_can_be_filtered_by_date(mongo, field):
    html = field.get("/surveys/?date=2026-10-07").data.decode()
    assert "sv-20261007-001" in html and "sv-20261006-001" not in html


def test_survey_detail_page_shows_the_survey(mongo, field):
    html = field.get("/surveys/sv-20261006-001").data.decode()
    assert "Outer Reef Drop-off" in html


def test_unknown_survey_is_a_404(mongo, field):
    assert field.get("/surveys/sv-19990101-001").status_code == 404


def test_unknown_page_shows_the_error_template(field):
    response = field.get("/no-such-page")
    assert response.status_code == 404 and b"404" in response.data


# ---------- entering a survey ----------


def valid_form(**overrides):
    form = {
        "surveyDate": NEW_DAY,
        "site": "North Reef Transect A",
        "totalCost": "450.00",
        "researcher_name": "Dr Test",
        "researcher_email": "",
        "species_name": ["Clownfish", ""],  # the blank row must be ignored
        "species_count": ["12", ""],
        "equipment_id": ["eq-06"],
        "equipment_qty": ["2"],
    }
    form.update(overrides)
    return form


def test_valid_survey_is_saved_and_stock_drops(mongo, field):
    before = stock(mongo, "eq-06")
    response = field.post("/surveys/new", data=valid_form())
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/surveys/sv-20261020-001")
    assert stock(mongo, "eq-06") == before - 2
    saved = mongo.surveys.find_one({"_id": "sv-20261020-001"})
    assert saved["species"] == [
        {"name": "Clownfish", "count": 12}
    ]  # strings became numbers
    assert saved["totalCost"] == 450.0
    assert (
        "email" not in saved["researcher"]
    )  # empty email is left out, not stored as ""


def test_invalid_survey_redisplays_the_form_with_errors(mongo, field):
    response = field.post("/surveys/new", data=valid_form(site=""))
    assert response.status_code == 400
    assert b"site" in response.data
    assert mongo.surveys.count_documents({"surveyDate": NEW_DAY}) == 0


def test_form_keeps_what_the_user_typed_after_an_error(mongo, field):
    html = field.post("/surveys/new", data=valid_form(site="")).data.decode()
    assert 'value="Dr Test"' in html and 'value="Clownfish"' in html


def test_not_enough_stock_shows_a_message_and_changes_nothing(mongo, field):
    before = stock(mongo, "eq-06")
    response = field.post("/surveys/new", data=valid_form(equipment_qty=["9999"]))
    assert response.status_code == 400
    assert b"Not enough" in response.data
    assert stock(mongo, "eq-06") == before


def test_non_numeric_count_is_reported_not_a_server_error(mongo, field):
    response = field.post("/surveys/new", data=valid_form(species_count=["lots", ""]))
    assert response.status_code == 400
    assert b"whole number" in response.data


def test_unknown_equipment_id_is_rejected(mongo, field):
    response = field.post("/surveys/new", data=valid_form(equipment_id=["eq-999"]))
    assert response.status_code == 400


# ---------- summaries ----------


def test_generate_with_invalid_date_is_refused(admin, monkeypatch):
    called = []
    monkeypatch.setattr(summary_service, "generate_summary", lambda d: called.append(d))
    monkeypatch.setattr(summary_service, "get_all_summaries", lambda: [])
    response = admin.post(
        "/summaries/generate", data={"date": "20261006"}, follow_redirects=True
    )
    assert called == []
    assert b"valid date" in response.data


def test_generate_success_goes_to_the_new_summary(admin, monkeypatch):
    monkeypatch.setattr(summary_service, "generate_summary", lambda d: None)
    response = admin.post("/summaries/generate", data={"date": "2026-10-06"})
    assert response.status_code == 302
    assert response.headers["Location"].endswith("/summaries/2026-10-06")


def test_generating_a_duplicate_is_reported(admin, monkeypatch):
    def duplicate(day):
        raise DuplicateSummary(day)

    monkeypatch.setattr(summary_service, "generate_summary", duplicate)
    monkeypatch.setattr(summary_service, "get_all_summaries", lambda: [])
    response = admin.post(
        "/summaries/generate", data={"date": "2026-10-06"}, follow_redirects=True
    )
    assert b"already exists" in response.data


def test_generating_for_a_day_without_surveys_is_reported(admin, monkeypatch):
    def none_found(day):
        raise NoSurveysForDate(day)

    monkeypatch.setattr(summary_service, "generate_summary", none_found)
    monkeypatch.setattr(summary_service, "get_all_summaries", lambda: [])
    response = admin.post(
        "/summaries/generate", data={"date": "2026-01-01"}, follow_redirects=True
    )
    assert b"No surveys were recorded" in response.data


@pytest.mark.parametrize("day", ["bad", "2026-13-01", "20261006"])
def test_summary_detail_rejects_malformed_dates(field, day):
    assert field.get(f"/summaries/{day}").status_code == 404


def test_summary_detail_for_a_missing_day_is_a_404(field, monkeypatch):
    monkeypatch.setattr(summary_service, "get_summary", lambda d: [])
    assert field.get("/summaries/2026-10-13").status_code == 404


# ---------- PDF report ----------


def test_survey_pdf_download(mongo, field):
    pytest.importorskip("reportlab")
    response = field.get("/surveys/sv-20261006-001/pdf")
    assert response.status_code == 200
    assert response.mimetype == "application/pdf"
    assert response.data.startswith(b"%PDF")


def test_pdf_for_unknown_survey_is_a_404(mongo, field):
    assert field.get("/surveys/sv-19990101-001/pdf").status_code == 404
