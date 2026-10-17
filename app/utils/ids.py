from uuid import uuid4


def new_id(prefix: str) -> str:
    return f"{prefix}-{uuid4().hex[:8]}"


def survey_id(survey_date: str, n: int) -> str:
    return f"sv-{survey_date.replace('-', '')}-{n:03d}"
