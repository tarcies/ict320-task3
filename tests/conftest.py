"""Shared fixtures.

The unit tests never touch Azure: MongoDB is replaced by an in-memory mongomock
database loaded from data/seed_data.json, and Azure SQL by a recording fake.
"""
import json
from pathlib import Path

import mongomock
import pytest

from app import create_app

SEED = json.loads((Path(__file__).resolve().parents[1] / "data" / "seed_data.json").read_text())

# Fresh day with no surveys in the seed data, so ID numbering starts at 001.
NEW_DAY = "2026-10-20"


@pytest.fixture
def mongo(monkeypatch):
    """In-memory copy of the seeded Mongo collections, wired into the services."""
    db = mongomock.MongoClient()["reefwatch_test"]
    db.equipment.insert_many(json.loads(json.dumps(SEED["equipment"])))
    db.surveys.insert_many(json.loads(json.dumps(SEED["surveys"])))
    monkeypatch.setattr("app.services.equipment_service.mongo_equipment", lambda: db.equipment)
    monkeypatch.setattr("app.services.survey_service.mongo_surveys", lambda: db.surveys)
    monkeypatch.setattr("app.services.summary_service.mongo_surveys", lambda: db.surveys)
    return db


class FakeSql:
    """Stands in for get_sql(): records every statement, can simulate a duplicate key."""

    def __init__(self):
        self.executed = []
        self.raise_on_execute = None

    def __call__(self):
        outer = self

        class Conn:
            def __enter__(self):
                return self

            def __exit__(self, *exc):
                return False

            def cursor(self):
                class Cursor:
                    def execute(self, *args):
                        outer.executed.append(args)
                        if outer.raise_on_execute:
                            raise outer.raise_on_execute

                return Cursor()

        return Conn()


@pytest.fixture
def fake_sql(monkeypatch):
    fake = FakeSql()
    monkeypatch.setattr("app.services.summary_service.get_sql", fake)
    return fake


@pytest.fixture
def client():
    app = create_app()
    app.config.update(TESTING=True)
    return app.test_client()


def _sign_in(client, role):
    with client.session_transaction() as s:
        s["user"] = {"id": 1, "username": f"test_{role}", "role": role}


# Note: `admin` and `field` share the `client` fixture, so use only one of them per test.
@pytest.fixture
def admin(client):
    _sign_in(client, "admin")
    return client


@pytest.fixture
def field(client):
    _sign_in(client, "field")
    return client


def make_survey(**overrides):
    """A valid survey document (as the route's form parser would build it)."""
    survey = {
        "surveyDate": NEW_DAY,
        "stationId": "STN-01",
        "site": "North Reef Transect A",
        "researcher": {"name": "Dr Test", "email": "test@example.org"},
        "species": [{"name": "Clownfish", "count": 12}],
        "equipmentUsed": [{"equipmentId": "eq-06", "name": "Dive Slate and Pencils", "quantity": 2}],
        "totalCost": 450.0,
    }
    survey.update(overrides)
    return survey


def stock(db, equipment_id):
    return db.equipment.find_one({"_id": equipment_id})["availableQuantity"]
