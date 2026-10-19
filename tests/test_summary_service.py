"""Daily summaries: the numbers come from MongoDB, the row goes to SQL.

Azure SQL is replaced by a fake that records the INSERT. Whether the database itself
rejects a second row for the same date is checked for real in tests/integration.
"""
import pytest

from app.services import summary_service
from app.utils.errors import DuplicateSummary, NoSurveysForDate


def test_summary_totals_are_calculated_from_the_days_surveys(mongo, fake_sql):
    summary_service.generate_summary("2026-10-06")
    assert len(fake_sql.executed) == 1
    statement = repr(fake_sql.executed[0])
    expected_cost = sum(s["totalCost"] for s in mongo.surveys.find({"surveyDate": "2026-10-06"}))
    assert str(expected_cost) in statement or f"{expected_cost:.2f}" in statement
    assert "Parrotfish" in statement  # the top species for that day in the seed data


def test_summary_counts_only_the_requested_day(mongo, fake_sql):
    summary_service.generate_summary("2026-10-07")
    args = fake_sql.executed[0]
    assert "2026-10-07" in repr(args)
    assert "2026-10-06" not in repr(args)


def test_summary_includes_low_stock_alerts(mongo, fake_sql):
    mongo.equipment.update_one({"_id": "eq-06"}, {"$set": {"availableQuantity": 0}})
    summary_service.generate_summary("2026-10-06")
    assert "Dive Slate and Pencils (0 left)" in repr(fake_sql.executed[0])


def test_day_without_surveys_is_refused(mongo, fake_sql):
    with pytest.raises(NoSurveysForDate):
        summary_service.generate_summary("2026-01-01")
    assert fake_sql.executed == []  # nothing is written


def test_existing_summary_is_reported_as_duplicate(mongo, fake_sql):
    fake_sql.raise_on_execute = summary_service.IntegrityError("duplicate key")
    with pytest.raises(DuplicateSummary):
        summary_service.generate_summary("2026-10-06")
