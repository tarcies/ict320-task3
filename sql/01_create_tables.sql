IF OBJECT_ID(N'dbo.DailySummaries', N'U') IS NULL
    BEGIN
        CREATE TABLE dbo.DailySummaries (
            Date               DATE            NOT NULL PRIMARY KEY,
            TotalSurveys       INT             NOT NULL CHECK (TotalSurveys >= 0),
            TotalSurveyCost    DECIMAL (12, 2) NOT NULL CHECK (TotalSurveyCost >= 0),
            TopSpecies         NVARCHAR (100)  NULL,
            TopSpeciesCount    INT             NULL,
            LowEquipmentAlerts NVARCHAR (100)  NULL,
            CreatedAt          DATETIME2       DEFAULT SYSDATETIME() NOT NULL
        );
    END