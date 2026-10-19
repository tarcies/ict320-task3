"""Survey validation: bad input must be rejected with readable messages."""
import copy

import pytest

from app.models import validate_survey
from app.utils.errors import ValidationError
from tests.conftest import make_survey


def test_valid_survey_passes():
    validate_survey(make_survey())  # must not raise


def test_email_is_optional():
    survey = make_survey(researcher={"name": "Dr Test"})
    validate_survey(survey)


@pytest.mark.parametrize(
    "change",
    [
        {"site": ""},                                       # blank site
        {"species": []},                                    # a survey needs at least one species
        {"species": [{"name": "Clownfish", "count": 0}]},   # count must be at least 1
        {"species": [{"name": "Clownfish", "count": -3}]},
        {"totalCost": -1},
        {"totalCost": "cheap"},
        {"surveyDate": "2026-13-45"},                       # not a real date
        {"surveyDate": "14/10/2026"},                       # wrong format
        {"researcher": {"name": ""}},
        {"researcher": {"name": "Dr Test", "email": "not-an-email"}},
        {"equipmentUsed": [{"equipmentId": "eq-01", "quantity": 0}]},
        {"unexpectedField": "x"},                           # additionalProperties is False
    ],
    ids=lambda c: next(iter(c)) + "=" + str(next(iter(c.values())))[:20],
)
def test_invalid_survey_is_rejected(change):
    with pytest.raises(ValidationError) as excinfo:
        validate_survey(make_survey(**change))
    messages = excinfo.value.args[0]
    assert isinstance(messages, list) and messages  # at least one readable message


def test_missing_required_field_is_rejected():
    survey = make_survey()
    del survey["site"]
    with pytest.raises(ValidationError):
        validate_survey(survey)


def test_all_errors_are_reported_together():
    survey = make_survey(site="", totalCost=-5)
    with pytest.raises(ValidationError) as excinfo:
        validate_survey(survey)
    assert len(excinfo.value.args[0]) >= 2  # the user sees every problem at once


def test_validation_does_not_modify_the_input():
    survey = make_survey()
    before = copy.deepcopy(survey)
    validate_survey(survey)
    assert survey == before
