from . import survey, equipment, partner
from jsonschema import Draft202012Validator, FormatChecker
from app.utils.errors import ValidationError

_VALIDATORS = {
    name: Draft202012Validator(module.schema, format_checker=FormatChecker())
    for name, module in (
        ("survey", survey),
        ("equipment", equipment),
        ("partner", partner),
    )
}


def validate_document(type, data):
    errors = sorted(_VALIDATORS[type].iter_errors(data), key=lambda e: list(e.path))
    if errors:
        raise ValidationError(
            [f"{'.'.join(map(str, e.path)) or 'document'}: {e.message}" for e in errors]
        )
    return data


def validate_survey(data):
    return validate_document("survey", data)


def validate_equipment(data):
    return validate_document("equipment", data)


def validate_partner(data):
    return validate_document("partner", data)
