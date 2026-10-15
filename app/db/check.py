from app.db.mongo import get_db
from app.db.sql import get_connection

print("Mongo collections:", get_db()._list_collection_names())

with get_connection() as conn:
    cur = conn.cursor()
    cur.execute("SELECT @@VERSION")
    print("SQL:", cur.fetchone()[0][:60])
