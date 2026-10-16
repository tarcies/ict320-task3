schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "surveyDate": {"type": "string", "format": "date"},
        "stationId": {"type": "string", "minLength": 1},
        "site": {"type": "string", "minLength": 1},
        "researcher": {
            "type": "object",
            "properties": {
                "id": {"type": "string"},
                "name": {"type": "string", "minLength": 1},
                "email": {"type": "string", "format": "email"},
            },
            "required": ["name"],
            "additionalProperties": False,
        },
        "species": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "name": {"type": "string", "minLength": 1},
                    "count": {"type": "number", "minimum": 1},
                },
                "required": ["name", "count"],
                "additionalProperties": False,
            },
        },
        "equipmentUsed": {
            "type": "array",
            "items": {
                "type": "object",
                "properties": {
                    "equipmentId": {"type": "string"},
                    "name": {"type": "string"},
                    "quantity": {"type": "number", "minimum": 1},
                },
                "required": ["equipmentId", "quantity"],
                "additionalProperties": False,
            },
        },
        "totalCost": {"type": "number", "minimum": 0},
    },
    "required": [
        "surveyDate",
        "stationId",
        "site",
        "researcher",
        "species",
        "totalCost",
    ],
    "additionalProperties": False,
}
