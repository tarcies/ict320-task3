import os
from dotenv import load_dotenv
import time
from datetime import datetime, timedelta
import json
from enum import Enum
import typing
import random
import bcrypt

from fastapi import FastAPI
from pydantic import BaseModel
from mssql_python import connect
from pymongo import MongoClient

from flask import Flask, request, redirect, render_template, session

# TODO: Separate Flask module
app = Flask(__name__)

try:
    mongo_client = MongoClient(os.getenv("AZURE_COSMOS_CONNECTIONSTRING"))
    print(os.getenv("AZURE_SQL_CONNECTIONSTRING"))
except Exception as e:
    print(f"DB Connection Error | An error occured: {e}")
finally:
    if "cursor" in locals():
        cursor.close

if __name__ == "__main__":
    app.run(debug=True)
