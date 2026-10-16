from pymongo import MongoClient
from app.config import Config

_client = None


def get_mongo():
    global _client
    if _client is None:
        try:
            _client = MongoClient(
                Config.MONGO_CONNECTION_STRING, serverSelectionTimeoutMS=5000
            )
            info = _client.server_info()
            print("Connected to Azure Cosmos DB for MongoDB")
            print(info)
        except Exception:
            print("Error connecting to Azure Cosmos DB for MongoDB")
            raise

    return _client[Config.MONGO_DB_NAME]


def surveys():
    return get_mongo()["surveys"]


def equipment():
    return get_mongo()["equipment"]


def partners():
    return get_mongo()["partners"]
