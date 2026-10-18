"""Dashboard (home page)."""

from flask import Blueprint, render_template
from app.services import equipment_service, summary_service, survey_service

bp = Blueprint("main", __name__)


@bp.route("/")
def index():
    """Overview: low-stock alerts, latest surveys and latest daily summaries."""
    return render_template(
        "dashboard.html",
        low_stock=equipment_service.get_low_quantity(),
        recent_surveys=survey_service.get_recent_surveys(5),
        recent_summaries=summary_service.get_recent_summaries(5),
    )
