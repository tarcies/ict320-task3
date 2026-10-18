from app.db.mongo import surveys as mongo_surveys
from app.db.sql import get_sql, sql_select
from app.utils.errors import NoSurveysForDate, DuplicateSummary
from app.services.equipment_service import get_low_quantity
from mssql_python import IntegrityError


def TOTALS_PIPELINE(date):
    return [
        {"$match": {"surveyDate": date}},
        {
            "$group": {
                "_id": None,
                "totalSurveys": {"$sum": 1},
                "totalCost": {"$sum": "$totalCost"},
            }
        },
    ]


def TOP_SPECIES_PIPELINE(date):
    return [
        {"$match": {"surveyDate": date}},
        {"$unwind": "$species"},
        {
            "$group": {
                "_id": "$species.name",
                "total": {"$sum": "$species.count"},
            },
        },
        {"$sort": {"total": -1}},
        {"$limit": 1},
    ]


def generate_summary(date):
    totals = next(iter(mongo_surveys().aggregate(TOTALS_PIPELINE(date))), None)
    if totals is None:
        raise NoSurveysForDate(date)
    top = next(iter(mongo_surveys().aggregate(TOP_SPECIES_PIPELINE(date))), None)
    alerts = (
        "; ".join(
            f"{i['name']} ({i['availableQuantity']} left)" for i in get_low_quantity()
        )
        or None
    )

    with get_sql() as conn:
        cursor = conn.cursor()
        try:
            cursor.execute(
                "INSERT INTO DailySummaries (SummaryDate, TotalSurveys, TotalSurveyCost, "
                "TopSpecies, TopSpeciesCount, LowEquipmentAlerts) VALUES (?, ?, ?, ?, ?, ?)",
                (
                    date,
                    totals["totalSurveys"],
                    totals["totalCost"],
                    top["_id"] if top else None,
                    top["total"] if top else None,
                    alerts,
                ),
            )
        except IntegrityError:
            raise DuplicateSummary(date)


def get_summary(date):
    return sql_select(f"SELECT * FROM dbo.DailySummaries WHERE SummaryDate = '{date}'")


def get_all_summaries():
    return sql_select("SELECT * FROM dbo.DailySummaries")


def get_recent_summaries(count):
    return sql_select(
        f"SELECT TOP {count} * FROM dbo.DailySummaries ORDER BY SummaryDate DESC"
    )
