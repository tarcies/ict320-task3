from app.db import load
from app.db.sql import get_sql
from mssql_python.exceptions import DataError, OperationalError
from app.services import (
    summary_service,
    survey_service,
    equipment_service,
    partner_service,
    auth_service,
)

OPTIONS = {
    1: "1. Run SQL script",
    2: "2. Load MongoDB documents",
    3: "3. Get summary for a date",
    4: "4. Get surveys",
    5: "5. Get equipment",
    6: "6. Get partners",
    7: "7. Create user",
}


def run():
    while True:
        print("Choose an option\n")
        for option in OPTIONS:
            print(OPTIONS[option])

        try:
            choice = int(input("\n> "))

            match (choice):
                case 1:
                    path = input(
                        "Input path to an .sql file from the root directory (Example: `sql/01_create_tables.sql`, `sql/02_sample_summaries.sql`) \n> "
                    )
                    load.load_sql(path)
                case 2:
                    path = input(
                        "Input path to a .json document from the root directory (Example: `data/seed_data.json`) \n> "
                    )
                    load.load_mongo(path)
                case 3:
                    try:
                        date = input(
                            "Input date (Format `%Y-%m-%d`, Example: `2026-10-07`) \n> "
                        )
                        print(summary_service.get_summary(date))
                    except DataError:
                        print(
                            f"Incorrect date fromat {'(don\'t include apostrophes)' if '"' in date else ''}"
                        )
                case 4:
                    print(survey_service.get_all_surveys())
                case 5:
                    print(equipment_service.get_all_equipment())
                case 6:
                    print(partner_service.get_all_partners())
                case 7:
                    username = input("> Username: ")
                    password = input("> Password: ")
                    role = input("> Role (field/admin): ")
                    auth_service.create_user(username, password, role)
                case _:
                    print(f"Unknown option {choice}")
        except ValueError:
            print("Input must be a number")

        print("\n---------------------------\n")


try:
    with get_sql():
        pass
    run()
except KeyboardInterrupt:
    pass
