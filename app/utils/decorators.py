from functools import wraps
from flask import session, redirect, url_for, abort


def role_required(*roles):
    def decorator(view):
        @wraps(view)
        def wrapped(*args, **kwargs):
            user = session.get("user")
            if user is None:
                return redirect(url_for("auth.login"))
            if user["role"] not in roles:
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return decorator
