"""Partners (read-only list)."""

from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.decorators import role_required

from app.services import partner_service

bp = Blueprint("partners", __name__, url_prefix="/partners")


@bp.route("/")
def list_partners():
    """All partners grouped by region."""
    partners = sorted(
        partner_service.get_all_partners(),
        key=lambda i: (i["region"], i["organisationName"]),
    )
    return render_template("partners/list.html", partners=partners)


@bp.route("/add", methods=["POST"])
@role_required("admin")
def add_partner(form):
    partner_service.add_partner(form)
    return redirect(url_for("partners"))


@bp.route("/remove", methods=["POST"])
@role_required("admin")
def remove_partner(partner_id):
    partner_service.delete_partner(partner_id)
    return redirect(url_for("partners"))
