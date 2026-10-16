from app.db.mongo import equipment as mongo_equipment
from app.models import validate_equipment
from app.utils.errors import InsufficientStock


def add_equipment(form):
    validate_equipment(form)
    mongo_equipment().insert_one(form)


def _update_stock(equipment_id: str, change: int):
    filter_by = {"id": equipment_id}
    projection = {"_id": 0, "availableQuantity": 1, "lowStockThreshold": 1}

    res = mongo_equipment().find(filter=filter_by, projection=projection)[0]

    new_qty = int(res["availableQuantity"]) + change
    low_stock_threshold = int(res["lowStockThreshold"])

    if new_qty < 0:
        raise InsufficientStock

    if new_qty <= low_stock_threshold:
        print(f"Low stock alert on equipment {equipment_id}")

    update = {"$inc": {"availableQuantity": change}}
    mongo_equipment().find_one_and_update(filter_by, update)


def increment(equipment_id: str, qty: int):
    _update_stock(equipment_id, qty)


def decrement(equipment_id: str, qty: int):
    _update_stock(equipment_id, -qty)


def get_low_stock():
    pass
