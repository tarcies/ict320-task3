schema = {
    "type": "object",
    "properties": {
        "id": {"type": "string"},
        "organisationName": {"type": "string"},
        "region": {"type": "string", "maxLength": 3},
        "contact": {
            "type": "object",
            "properties": {
                "name": {"type": "string"},
                "email": {"type": "string", "format": "email"},
                "phone": {
                    "type": "string",
                    "pattern": r"^(?:\+61|0)[23478](?:[ -]?\d){8}$",
                },
            },
        },
        "conservationAreas": {"type": "array"},
    },
    "required": ["organisationName", "region", "contact"],
    "additionalProperties": False,
}
