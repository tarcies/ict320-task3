from flask import Blueprint, render_template, request, redirect, url_for, flash, abort
from app.utils.decorators import role_required
from app.utils.datetime import is_iso_date
from app.utils.errors import DuplicateSummary, NoSurveysForDate
from app.services import summary_service, survey_service

bp = Blueprint("summaries", __name__, url_prefix="/summaries")


@bp.route("/")
def list_summaries():
    return render_template(
        "summaries/list.html", summaries=summary_service.get_all_summaries()
    )


@bp.route("/generate", methods=["POST"])
@role_required("admin")
def generate():
    day = request.form.get("date", "").strip()

    if not is_iso_date(day):
        flash("Choose a valid date", "danger")
        return redirect(url_for("summaries.list_summaries"))

    try:
        summary_service.generate_summary(day)
    except DuplicateSummary:
        flash(f"A summary for {day} already exists", "warning")
    except NoSurveysForDate:
        flash(f"No surveys were recorded on {day}", "warning")
    else:
        flash(f"Summary for {day} generated", "info")
        return redirect(url_for("summaries.detail", day=day))
    return redirect(url_for("summaries.list_summaries"))


@bp.route("/<day>")
def detail(day):
    if not is_iso_date(day):
        abort(404)
    summary = summary_service.get_summary(day)
    if not summary:
        abort(404)
    return render_template(
        "summaries/detail.html",
        summary=summary,
        surveys=survey_service.get_all_surveys({"surveyDate": day}),
    )
