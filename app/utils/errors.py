from flask import redirect, request, url_for, flash


class InsufficientStock(Exception): ...


class DuplicateSummary(Exception): ...


class ValidationError(Exception): ...


class NoSurveysForDate(Exception): ...


def register_error_handlers(app):
    @app.errorhandler(InsufficientStock)
    def _stock(e):
        flash("Not enough equipment available", "danger")
        return redirect(request.referrer or url_for("main.index"))

    @app.errorhandler(DuplicateSummary)
    def _summary(e):
        flash("A summary for this date already exists", "danger")
        return redirect(request.referrer or url_for("main.index"))

    @app.errorhandler(ValidationError)
    def _validation(e):
        flash("The format of the input data is invalid", "danger")
        return redirect(request.referrer or url_for("main.index"))
