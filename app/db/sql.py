from contextlib import contextmanager
from mssql_python import connect
from app.config import Config


# Server=unisc.database.windows.net;Database=tp-task3;UID=dbconnection;PWD=aXEMHmMW84P7u9F;Encrypt=yes;TrustServerCertificate=no;
@contextmanager
def get_connection():
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
