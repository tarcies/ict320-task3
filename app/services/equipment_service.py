from app.db.mongo import equipment as mongo_equipment
from app.models import validate_equipment
from app.utils.errors import InsufficientStock
from app.utils.ids import new_id


def add_equipment(form):
    doc = {**validate_equipment(form), "_id": new_id("eq")}
    mongo_equipment().insert_one(doc)
    return doc["_id"]


def update_equipment(form):
    validate_equipment(form)
    mongo_equipment().replace_one({"_id": form["_id"]}, form)


def delete_equipment(equipment_id: str):
    mongo_equipment().delete_one({"_id": equipment_id})


def decrement(equipment_id, qty):
    res = mongo_equipment().update_one(
        {"_id": equipment_id, "availableQuantity": {"$gte": qty}},
        {"$inc": {"availableQuantity": -qty}},
    )
    if res.matched_count == 0:
        raise InsufficientStock(equipment_id)


def increment(equipment_id, qty):
    mongo_equipment().update_one(
        {"_id": equipment_id}, {"$inc": {"availableQuantity": qty}}
    )


def get_low_quantity():
    res = mongo_equipment().find(
        {"$expr": {"$lte": ["$availableQuantity", "$lowStockThreshold"]}},
        projection={"_id": 0, "name": 1, "availableQuantity": 1},
    )
    low_equipment = []
    for item in res:
        low_equipment.append(item)

    return low_equipment


def get_all_equipment(filter=None):
    return list(mongo_equipment().find(filter or {}))


def get_equipment(equipment_id):
    return mongo_equipment().find_one({"_id": equipment_id})  # None if missing


# # print(get_all_equipment())  # returns all equipment as array
# print(
#     get_equipment_by({"category": "Imaging"})
# )  # returns array of equipment from category "Imaging"
# print(
#     get_equipment_by({"$expr": {"$lte": ["$availableQuantity", "$lowStockThreshold"]}})
# )  # returns array of low stock equipment
# print(get_equipment_by({"test": "example"}))  # returns 0
# print(get_equipment("eq-05"))  # returns object of "Water Quality Probe"
# print(get_equipment("eq-123"))  # returns 0
