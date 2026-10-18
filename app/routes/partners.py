from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.decorators import role_required

bp = Blueprint("partners", __name__, url_prefix="/partners")


@bp.route("/")
def list_items():
    items = service.get_all_items()  # always a list
    return render_template("items/list.html", items=items)


@bp.route("/")
def list_items():
    items = service.get_all_items()  # always a list
    return render_template("items/list.html", items=items)


@bp.route("/")
def list_items():
    items = service.get_all_items()  # always a list
    return render_template("items/list.html", items=items)
