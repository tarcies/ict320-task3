"""Equipment stock rules."""
import pytest

from app.services import equipment_service
from app.utils.errors import InsufficientStock
from tests.conftest import stock


def test_decrement_reduces_stock(mongo):
    before = stock(mongo, "eq-06")
    equipment_service.decrement("eq-06", 3)
    assert stock(mongo, "eq-06") == before - 3


def test_decrement_to_exactly_zero_is_allowed(mongo):
    equipment_service.decrement("eq-06", stock(mongo, "eq-06"))
    assert stock(mongo, "eq-06") == 0


def test_decrement_beyond_stock_is_refused_and_changes_nothing(mongo):
    before = stock(mongo, "eq-06")
    with pytest.raises(InsufficientStock):
        equipment_service.decrement("eq-06", before + 1)
    assert stock(mongo, "eq-06") == before


def test_increment_restores_stock(mongo):
    before = stock(mongo, "eq-06")
    equipment_service.decrement("eq-06", 2)
    equipment_service.increment("eq-06", 2)
    assert stock(mongo, "eq-06") == before


def test_low_stock_lists_items_at_or_below_threshold(mongo):
    low = {item["name"] for item in equipment_service.get_low_quantity()}
    expected = {
        e["name"] for e in mongo.equipment.find({}) if e["availableQuantity"] <= e["lowStockThreshold"]
    }
    assert low == expected and low  # the seed data contains low-stock items


def test_item_drops_into_low_stock_after_use(mongo):
    item = mongo.equipment.find_one({"_id": "eq-06"})
    equipment_service.decrement("eq-06", item["availableQuantity"] - item["lowStockThreshold"])
    assert "Dive Slate and Pencils" in {i["name"] for i in equipment_service.get_low_quantity()}
