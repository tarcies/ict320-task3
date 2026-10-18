import os
from dotenv import load_dotenv

load_dotenv()


class Config:
    MONGO_CONNECTION_STRING = os.environ["MONGO_CONNECTION_STRING"]
    MONGO_DB_NAME = os.getenv("MONGO_DB_NAME", "reefwatch")
    SQL_CONNECTION_STRING = os.environ["SQL_CONNECTION_STRING"]
    SECRET_KEY = os.getenv("SECRET_KEY", "dev-only-change-this")
