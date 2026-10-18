from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from app.services.auth_service import create_user, authenticate
from app.utils.errors import DuplicateUser

bp = Blueprint("auth", __name__)


@bp.route("/login", methods=["GET", "POST"])
def login():
    if "user" in session:
        return redirect(url_for("main.index"))

    if request.method == "POST":
        user = authenticate(
            request.form.get("username", "").strip(), request.form.get("password", "")
        )
        if user:
            session.clear()
            session["user"] = user
            return redirect(url_for("main.index"))
        flash("Invalid username or password", "danger")
        return render_template("login.html"), 401

    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    flash("You have been signed out", "info")
    return redirect(url_for("auth.login"))


@bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        try:
            create_user(request.form["username"].strip(), request.form["password"])
            flash("Successfuly signed up", "info")
        except DuplicateUser:
            flash("Username is already taken", "danger")
            return render_template("signup.html"), 401
    return render_template("signup.html")
