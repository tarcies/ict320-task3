import time
from contextlib import contextmanager
from mssql_python import connect, OperationalError
from app.config import Config


def _connect(max_wait=120, delay=5):
    deadline = time.monotonic() + max_wait
    while True:
        try:
            return connect(Config.SQL_CONNECTION_STRING)
        except OperationalError as e:
            if time.monotonic() >= deadline:
                raise ConnectionError(
                    f"Azure SQL did not respond within {max_wait}s: {e}"
                ) from e
            print("Waiting for the database to resume...")
            time.sleep(delay)


@contextmanager
def get_sql():
    conn = _connect()
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
