from flask import Flask, request, session, redirect, url_for
from app.config import Config
from app.utils.errors import register_error_handlers
from app.services import auth_service
from app.routes import (
    main,
    surveys,
    equipment,
    partners,
    summaries,
    charts,
    auth,
)


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    for module in (main, surveys, equipment, partners, summaries, charts, auth):
        app.register_blueprint(module.bp)

    register_error_handlers(app)

    app.secret_key = Config.SECRET_KEY
    app.config.update(SESSION_COOKIE_SAMESITE="Lax")

    PUBLIC = {"auth.login", "auth.signup", "static"}

    @app.errorhandler(403)
    @app.errorhandler(404)
    @app.errorhandler(500)
    def http_error(e):
        return render_template("error.html", error=e), e.code

    @app.before_request
    def require_login():
        if request.endpoint is None or request.endpoint in PUBLIC:
            return

        if not "user" in session:
            return redirect(url_for("auth.login"))

    @app.context_processor
    def inject_user():
        if "user" in session:
            username = session.get("user")["username"]
            return {"user": username, "is_admin": auth_service.is_admin(username)}
        return {"user": None}

    return app
