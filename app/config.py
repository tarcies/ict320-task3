import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_CONNECTION_STRING = os.environ["MONGO_CONNECTION_STRING"]
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "reefwatch")
    SQL_SERVER = os.environ["SQL_SERVER"]
    SQL_DATABASE = os.environ["SQL_DATABASE"]
    SQL_USER = os.environ["SQL_USER"]
    SQL_PASSWORD = os.environ["SQL_PASSWORD"]
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this")
