-- Sample daily summaries for ReefWatch (run after 01_create_tables.sql).
-- Values were computed from data/seed_data.json, so they match what the aggregation
-- pipelines produce. Safe to re-run: existing dates are skipped.
-- 2026-10-12 and 2026-10-14 have surveys but NO summary, so you can generate them live.
-- 2026-10-11 and 2026-10-13 have no surveys (empty-day test case).
IF NOT EXISTS (SELECT 1
               FROM   dbo.DailySummaries
               WHERE  SummaryDate = '2026-10-06')
    INSERT  INTO dbo.DailySummaries (
        SummaryDate,
        TotalSurveys,
        TotalSurveyCost,
        TopSpecies,
        TopSpeciesCount,
        LowEquipmentAlerts
    )
    VALUES                          ('2026-10-06', 3, 2202.50, N'Parrotfish', 19, N'Water Quality Probe (2 left)');

IF NOT EXISTS (SELECT 1
               FROM   dbo.DailySummaries
               WHERE  SummaryDate = '2026-10-07')
    INSERT  INTO dbo.DailySummaries (
        SummaryDate,
        TotalSurveys,
        TotalSurveyCost,
        TopSpecies,
        TopSpeciesCount,
        LowEquipmentAlerts
    )
    VALUES                          ('2026-10-07', 2, 1100.00, N'Parrotfish', 19, N'Water Quality Probe (2 left)');

IF NOT EXISTS (SELECT 1
               FROM   dbo.DailySummaries
               WHERE  SummaryDate = '2026-10-08')
    INSERT  INTO dbo.DailySummaries (
        SummaryDate,
        TotalSurveys,
        TotalSurveyCost,
        TopSpecies,
        TopSpeciesCount,
        LowEquipmentAlerts
    )
    VALUES                          ('2026-10-08', 3, 1592.50, N'Blacktip Reef Shark', 29, N'Water Quality Probe (2 left)');

IF NOT EXISTS (SELECT 1
               FROM   dbo.DailySummaries
               WHERE  SummaryDate = '2026-10-09')
    INSERT  INTO dbo.DailySummaries (
        SummaryDate,
        TotalSurveys,
        TotalSurveyCost,
        TopSpecies,
        TopSpeciesCount,
        LowEquipmentAlerts
    )
    VALUES                          ('2026-10-09', 2, 947.50, N'Clownfish', 22, N'Water Quality Probe (2 left)');

IF NOT EXISTS (SELECT 1
               FROM   dbo.DailySummaries
               WHERE  SummaryDate = '2026-10-10')
    INSERT  INTO dbo.DailySummaries (
        SummaryDate,
        TotalSurveys,
        TotalSurveyCost,
        TopSpecies,
        TopSpeciesCount,
        LowEquipmentAlerts
    )
    VALUES                          ('2026-10-10', 3, 1497.50, N'Parrotfish', 17, N'Water Quality Probe (2 left); Tablet Housing (2 left)');