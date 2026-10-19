from flask import Blueprint, render_template, request, redirect, url_for, flash
from app.utils.decorators import role_required

bp = Blueprint("charts", __name__, url_prefix="/api/charts")


@bp.route("/surveys-per-day")
def surveys(day): ...


@bp.route("/species-total")
def species(): ...


@bp.route("/cost-per-day")
def cost(day): ...
