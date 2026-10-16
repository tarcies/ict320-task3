import pymssql
from reefwatch.db import mongo
from reefwatch.db.sql import get_connection
from reefwatch.utils.errors import DuplicateSummary


def generate_summary(date):
    # 1. Mongo: the aggregation runs inside the database
    totals = list(
        mongo.surveys().aggregate(
            [
                {"$match": {"surveyDate": date}},
                {
                    "$group": {
                        "_id": None,
                        "totalSurveys": {"$sum": 1},
                        "totalCost": {"$sum": "$totalCost"},
                    }
                },
            ]
        )
    )

    top = list(
        mongo.surveys().aggregate(
            [
                {"$match": {"surveyDate": date}},
                {"$unwind": "$species"},
                {
                    "$group": {
                        "_id": "$species.name",
                        "total": {"$sum": "$species.count"},
                    }
                },
                {"$sort": {"total": -1}},
                {"$limit": 1},
            ]
        )
    )

    # 2. SQL: write one row, and let the primary key reject duplicates
    with get_connection() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO DailySummary (SummaryDate, TotalSurveys, TotalSurveyCost, "
                "TopSpecies, TopSpeciesCount) VALUES (%s, %s, %s, %s, %s)",
                (
                    date,
                    totals[0]["totalSurveys"],
                    totals[0]["totalCost"],
                    top[0]["_id"],
                    top[0]["total"],
                ),
            )
        except pymssql.IntegrityError:
            raise DuplicateSummary(date)
