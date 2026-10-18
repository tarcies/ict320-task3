"""Equipment (read-only list; stock changes happen when surveys are saved)."""

from flask import Blueprint, render_template

from app.services import equipment_service

bp = Blueprint("equipment", __name__, url_prefix="/equipment")


@bp.route("/")
def list_equipment():
    """All equipment grouped by category; the template highlights low stock."""
    items = sorted(
        equipment_service.get_all_equipment(), key=lambda i: (i["category"], i["name"])
    )
    return render_template("equipment/list.html", items=items)
