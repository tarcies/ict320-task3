schema = {
    "type": "object",
    "properties": {
        "organisationName": {"type": "string"},
        "region": {
            "type": "string",
            "enum": ["NSW", "VIC", "QLD", "WA", "SA", "TAS", "ACT", "NT", "Other"],
        },
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
