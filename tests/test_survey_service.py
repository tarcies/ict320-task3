"""Saving surveys: IDs, stock updates and rollback."""
import pytest

from app.services import survey_service
from app.utils.errors import InsufficientStock, ValidationError
from tests.conftest import NEW_DAY, make_survey, stock


def test_first_survey_of_a_day_gets_number_001(mongo):
    assert survey_service.add_survey(make_survey()) == "sv-20261020-001"


def test_ids_count_up_within_a_day_and_restart_on_a_new_day(mongo):
    assert survey_service.add_survey(make_survey()) == "sv-20261020-001"
    assert survey_service.add_survey(make_survey()) == "sv-20261020-002"
    assert survey_service.add_survey(make_survey(surveyDate="2026-10-21")) == "sv-20261021-001"


def test_id_collision_is_retried_with_the_next_number(mongo):
    # One survey exists for the day (count says next is 002) but 002 is already taken.
    mongo.surveys.insert_one(make_survey(_id="sv-20261020-002"))
    assert survey_service.add_survey(make_survey()) == "sv-20261020-003"


def test_saved_survey_has_createdat_and_is_stored(mongo):
    survey_id = survey_service.add_survey(make_survey())
    doc = mongo.surveys.find_one({"_id": survey_id})
    assert doc["site"] == "North Reef Transect A"
    assert doc["createdAt"].endswith("Z")


def test_saving_a_survey_takes_the_equipment_from_stock(mongo):
    before = stock(mongo, "eq-06")
    survey_service.add_survey(make_survey())
    assert stock(mongo, "eq-06") == before - 2


def test_not_enough_stock_rejects_the_survey_and_saves_nothing(mongo):
    survey = make_survey(equipmentUsed=[{"equipmentId": "eq-06", "name": "x", "quantity": 9999}])
    with pytest.raises(InsufficientStock):
        survey_service.add_survey(survey)
    assert mongo.surveys.count_documents({"surveyDate": NEW_DAY}) == 0


def test_failure_on_a_later_item_puts_earlier_items_back(mongo):
    before = stock(mongo, "eq-06")
    survey = make_survey(
        equipmentUsed=[
            {"equipmentId": "eq-06", "name": "Dive Slate and Pencils", "quantity": 2},  # fine
            {"equipmentId": "eq-05", "name": "Water Quality Probe", "quantity": 9999},  # fails
        ]
    )
    with pytest.raises(InsufficientStock):
        survey_service.add_survey(survey)
    assert stock(mongo, "eq-06") == before  # the first item was rolled back
    assert mongo.surveys.count_documents({"surveyDate": NEW_DAY}) == 0


def test_invalid_survey_is_rejected_before_touching_stock(mongo):
    before = stock(mongo, "eq-06")
    with pytest.raises(ValidationError):
        survey_service.add_survey(make_survey(site=""))
    assert stock(mongo, "eq-06") == before


def test_get_survey_returns_none_for_unknown_id(mongo):
    assert survey_service.get_survey("sv-19990101-001") is None


def test_surveys_can_be_filtered_by_date(mongo):
    rows = survey_service.get_surveys_by({"surveyDate": "2026-10-06"})
    assert len(rows) == 3 and all(r["surveyDate"] == "2026-10-06" for r in rows)
