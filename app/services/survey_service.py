from app.db.mongo import surveys as mongo_surveys
from app.models import validate_survey
from . import equipment_service
from pymongo.errors import DuplicateKeyError
from app.utils import ids, datetime


def _insert_with_date_id(doc):
    n = mongo_surveys().count_documents({"surveyDate": doc["surveyDate"]}) + 1

    while True:
        doc["_id"] = ids.survey_id(doc["surveyDate"], n)
        try:
            mongo_surveys().insert_one(doc)
            return doc["_id"]
        except DuplicateKeyError:
            n += 1  # Duplicate ID => increase n and try again


def create_survey(form):
    doc = {**validate_survey(form), "createdAt": datetime.utc_now_iso()}

    reserved = []
    try:
        for item in doc["equipmentUsed"]:
            equipment_service.decrement(item["equipmentId"], item["quantity"])
            reserved.append(item)

        return _insert_with_date_id(doc)

    except Exception:
        # Revert equipment stock if an error occurs after the stock has already been updated
        for item in reserved:
            equipment_service.increment(item["equipmentId"], item["quantity"])
        raise


def get_all_surveys(filter=None):
    return list(mongo_surveys().find(filter or {}).sort({"surveyDate": -1}))


def get_recent_surveys(count):
    return list(mongo_surveys().find(limit=count).sort({"surveyDate": -1}))


def get_survey(survey_id):
    return mongo_surveys().find_one({"_id": survey_id})  # None if missing
