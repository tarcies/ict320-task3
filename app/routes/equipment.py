"""Equipment (read-only list; stock changes happen when surveys are saved)."""

from flask import Blueprint, render_template
from app.utils.decorators import role_required

from app.services import equipment_service

bp = Blueprint("equipment", __name__, url_prefix="/equipment")


@bp.route("/")
def list_equipment():
    """All equipment grouped by category; the template highlights low stock."""
    items = sorted(
        equipment_service.get_all_equipment(), key=lambda i: (i["category"], i["name"])
    )
    return render_template("equipment/list.html", items=items)


@bp.route("/add", methods=["POST"])
@role_required("admin")
def add_equipment(form):
    equipment_service.add_equipment(form)
    return redirect(url_for("partners"))


@bp.route("/remove", methods=["POST"])
@role_required("admin")
def remove_equipment(equipment_id):
    equipment_service.delete_equipment(equipment_id)
    return redirect(url_for("partners"))
