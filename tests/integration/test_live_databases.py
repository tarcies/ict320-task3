"""Runs against the REAL Azure databases. Spends RU/credits, so it is skipped by default.

    pytest -m integration

Needs the same environment variables / .env as the app. It writes one summary row and
removes it again. Pick a day that has surveys but no summary yet (2026-10-12 in the
sample data) and change DAY below if you already generated it.
"""
import pytest

from app.db.sql import get_sql
from app.services import summary_service
from app.utils.errors import DuplicateSummary

pytestmark = pytest.mark.integration

DAY = "2026-10-12"


@pytest.fixture
def clean_summary():
    def delete():
        with get_sql() as conn:
            conn.cursor().execute("DELETE FROM DailySummaries WHERE SummaryDate = ?", (DAY,))

    delete()
    yield
    delete()


def test_second_summary_for_the_same_day_is_rejected_by_the_database(clean_summary):
    summary_service.generate_summary(DAY)          # first time: stored
    with pytest.raises(DuplicateSummary):
        summary_service.generate_summary(DAY)      # second time: the unique constraint refuses it
    assert len(summary_service.get_summary(DAY)) == 1
