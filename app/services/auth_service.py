from werkzeug.security import generate_password_hash, check_password_hash
from mssql_python import IntegrityError
from app.db.sql import get_sql, sql_select
from app.utils.errors import DuplicateUser

ROLES = ("admin", "field")


def create_user(username, password, role="field"):
    if role not in ROLES:
        raise ValueError(f"role must be one of {ROLES}")
    with get_sql() as conn:
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO Users (Username, PasswordHash, Role) VALUES (?, ?, ?)",
                (username, generate_password_hash(password), role),
            )
        except IntegrityError:
            raise DuplicateUser(username)


def authenticate(username, password):
    with get_sql() as conn:
        cur = conn.cursor()
        cur.execute(
            "SELECT UserId, Username, PasswordHash, Role FROM Users WHERE Username = ?",
            (username,),
        )
        row = cur.fetchone()
    if row and check_password_hash(row[2], password):
        return {"id": row[0], "username": row[1], "role": row[3]}
    return None


def is_admin(username):
    role = sql_select(f"SELECT Role FROM dbo.Users WHERE Username = '{username}'")
    if role:
        return bool(role["Role"] == "admin")
    return False
