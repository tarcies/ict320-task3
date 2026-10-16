from app.db.mongo import get_mongo
from app.db.sql import get_sql

print("Mongo collections:", get_mongo()._list_collection_names())

with get_sql() as conn:
    cur = conn.cursor()
    cur.execute("SELECT @@VERSION")
    print("SQL:", cur.fetchone()[0][:60])
