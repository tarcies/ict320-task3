from datetime import date, datetime, timezone


def utc_now_iso():
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


def is_iso_date(text):
    try:
        return date.fromisoformat(text).isoformat() == text
    except (TypeError, ValueError):
        return False
