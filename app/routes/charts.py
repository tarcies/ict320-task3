from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.decorators import role_required

bp = Blueprint("charts", __name__, url_prefix="/api/charts")


@bp.route("/surveys-per-day")
def list_items():
    items = service.get_all_items()  # always a list
    return render_template("items/list.html", items=items)


@bp.route("/species-total")
def list_items():
    items = service.get_all_items()  # always a list
    return render_template("items/list.html", items=items)


@bp.route("/cost-per-day")
def list_items():
    items = service.get_all_items()  # always a list
    return render_template("items/list.html", items=items)
