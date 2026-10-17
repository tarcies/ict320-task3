from . import sql
from . import mongo
from json import loads as json_loads
from time import sleep


def _read_file(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            data = file.read()
            return data
    except FileNotFoundError:
        print(f"{path} was not found")


def load_sql(path):
    sql_script = _read_file(path)
    with sql.get_sql() as conn:
        cursor = conn.cursor()
        cursor.execute(sql_script)


def load_mongo(path):
    json_data = json_loads(_read_file(path))

    surveys = json_data["surveys"]
    equipment = json_data["equipment"]
    partners = json_data["partners"]

    if surveys:
        for survey in surveys:
            print(f"MONGODB > Inserting survey for: {survey["surveyDate"]}")
            sleep(0.5)
            mongo.surveys().insert_one(survey)

    if equipment:
        for equip in equipment:
            print(f"MONGODB > Inserting equipment: {equip["name"]}")
            sleep(0.5)
            mongo.equipment().insert_one(equip)

    if partners:
        for partner in partners:
            print(f"MONGODB > Inserting partner: {partner["organisationName"]}")
            sleep(0.5)
            mongo.partners().insert_one(partner)
