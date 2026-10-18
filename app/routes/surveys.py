import io
from flask import (
    Blueprint,
    abort,
    flash,
    redirect,
    render_template,
    request,
    url_for,
    send_file,
)

from app.services import equipment_service, survey_service
from app.utils.datetime import is_iso_date
from app.utils.errors import InsufficientStock, ValidationError

bp = Blueprint("surveys", __name__, url_prefix="/surveys")

STATION_ID = "STN-01"  # this PoC covers a single monitoring station


def _whole_number(value, label):
    """Convert a form string to int, with a readable error if it isn't one."""
    try:
        return int(value)
    except (TypeError, ValueError):
        raise ValueError(f"{label} must be a whole number") from None


def _parse_survey_form(form, catalog):
    """Turn the submitted HTML form into the dict validate_survey() expects."""
    species = []
    for name, count in zip(form.getlist("species_name"), form.getlist("species_count")):
        name = name.strip()
        if name:  # skip blank rows
            species.append(
                {"name": name, "count": _whole_number(count, f"Count for {name}")}
            )

    equipment_used = []
    for eq_id, qty in zip(form.getlist("equipment_id"), form.getlist("equipment_qty")):
        if not eq_id:
            continue
        if eq_id not in catalog:
            raise ValueError(f"Unknown equipment: {eq_id}")
        equipment_used.append(
            {
                "equipmentId": eq_id,
                "name": catalog[eq_id][
                    "name"
                ],  # stored with the survey, as in the seed data
                "quantity": _whole_number(
                    qty, f"Quantity for {catalog[eq_id]['name']}"
                ),
            }
        )

    researcher = {"name": form.get("researcher_name", "").strip()}
    email = form.get("researcher_email", "").strip()
    if email:  # an empty string would fail the email format check
        researcher["email"] = email

    try:
        total_cost = float(form.get("totalCost", ""))
    except ValueError:
        raise ValueError("Total cost must be a number") from None

    return {
        "surveyDate": form.get("surveyDate", ""),
        "stationId": form.get("stationId", STATION_ID),
        "site": form.get("site", "").strip(),
        "researcher": researcher,
        "species": species,
        "equipmentUsed": equipment_used,
        "totalCost": total_cost,
    }


@bp.route("/")
def list_surveys():
    """List surveys, newest first; optionally filter with ?date=YYYY-MM-DD."""
    day = request.args.get("date", "").strip()

    if day and not is_iso_date():
        flash("Date must be in YYYY-MM-DD format", "warning")

    surveys = (
        survey_service.get_all_surveys({"surveyDate": day})
        if day
        else survey_service.get_all_surveys()
    )
    return render_template("surveys/list.html", surveys=surveys, day=day)


@bp.route("/new", methods=["GET", "POST"])
def new_survey():
    """Show the entry form; on POST validate, save and redirect to the new survey."""
    equipment_items = equipment_service.get_all_equipment()
    catalog = {item["_id"]: item for item in equipment_items}

    if request.method == "POST":
        try:
            survey_id = survey_service.add_survey(
                _parse_survey_form(request.form, catalog)
            )
        except ValidationError as e:
            for message in e.args[0]:
                flash(message, "danger")
        except InsufficientStock as e:
            eq_id = e.args[0] if e.args else ""
            name = catalog.get(eq_id, {}).get("name", "equipment")
            flash(f"Not enough {name} in stock", "danger")
        except ValueError as e:
            flash(str(e), "danger")
        else:
            flash(f"Survey {survey_id} saved", "success")
            return redirect(url_for("surveys.detail", survey_id=survey_id))
        # Any failure: redisplay the form with what the user typed
        return (
            render_template(
                "surveys/new.html", equipment=equipment_items, form=request.form
            ),
            400,
        )

    return render_template("surveys/new.html", equipment=equipment_items, form={})


@bp.route("/<survey_id>")
def detail(survey_id):
    survey = survey_service.get_survey(survey_id)
    if survey is None:
        abort(404)
    return render_template("surveys/detail.html", survey=survey)


@bp.route("/<survey_id>/pdf")
def pdf(survey_id):
    """Download a survey report."""
    from app.services import report_service

    survey = survey_service.get_survey(survey_id)
    if survey is None:
        abort(404)
    return send_file(
        io.BytesIO(report_service.survey_pdf(survey)),
        mimetype="application/pdf",
        download_name=f"{survey_id}.pdf",
    )
