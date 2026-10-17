from app.db.mongo import partners as mongo_partners
from app.models import validate_partner
from app.utils.ids import new_id


def add_partner(form):
    doc = {**validate_partner(form), "_id": new_id("po")}
    mongo_partners().insert_one(doc)
    return doc["_id"]


def update_partner(form):
    validate_partner(form)
    mongo_partners().replace_one({"_id": form["_id"]}, form)


def delete_partner(partner_id: str):
    mongo_partners().delete_one({"_id": partner_id})


def add_area(partner_id, new_areas):
    areas = [new_areas] if isinstance(new_areas, str) else list(new_areas)
    res = mongo_partners().update_one(
        {"_id": partner_id}, {"$addToSet": {"conservationAreas": {"$each": areas}}}
    )
    if res.matched_count == 0:
        raise NotFound(partner_id)


def get_all_partners(filter=None):
    return list(mongo_partners().find(filter or {}))


def get_partner(partner_id):
    return mongo_partners().find_one({"_id": partner_id})  # None if missing
