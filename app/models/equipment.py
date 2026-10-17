schema = {
    "type": "object",
    "properties": {
        "name": {"type": "string"},
        "category": {"type": "string"},
        "replacementCost": {"type": "number", "minimum": 0},
        "availableQuantity": {"type": "number", "minimum": 0},
        "lowStockThreshold": {"type": "number", "minimum": 0},
    },
    "required": ["name"],
    "additionalProperties": False,
}
