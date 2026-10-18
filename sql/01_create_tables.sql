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

IF OBJECT_ID(N'dbo.Users', N'U') IS NULL
    BEGIN
        CREATE TABLE dbo.Users (
            UserId       INT            IDENTITY (1, 1) PRIMARY KEY,
            Username     NVARCHAR (50)  NOT NULL UNIQUE,
            PasswordHash NVARCHAR (255) NOT NULL,
            Role         NVARCHAR (20)  NOT NULL CHECK (Role IN ('admin', 'field')),
            CreatedAt    DATETIME2      DEFAULT SYSUTCDATETIME() NOT NULL
        );
    END