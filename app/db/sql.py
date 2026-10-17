from contextlib import contextmanager
from mssql_python import connect
from app.config import Config


@contextmanager
def get_sql():
    conn_str = f"Server={Config.SQL_SERVER};Database={Config.SQL_DATABASE};UID={Config.SQL_USER};PWD={Config.SQL_PASSWORD};Encrypt=yes;TrustServerCertificate=no;"

    conn = connect(conn_str)

    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()


def sql_select(query):
    with get_sql() as conn:
        cursor = conn.cursor()
        cursor.execute(query)
        columns = [col[0] for col in cursor.description]
        fetch = [dict(zip(columns, row)) for row in cursor.fetchall()]
        if len(fetch) == 1:
            fetch = fetch[0]
        return fetch
