"""
JWT authentication service.
"""
import datetime

import jwt
from passlib.hash import bcrypt

from app.config import SECRET_KEY, JWT_ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
from app.db.database import get_connection


def authenticate_user(email: str, password: str) -> dict | None:
    """Verify credentials. Returns user dict or None."""
    conn = get_connection()
    row = conn.execute(
        "SELECT id, email, full_name, role, password_hash, created_at FROM users WHERE email = ?",
        (email,),
    ).fetchone()
    conn.close()

    if not row:
        return None

    if not bcrypt.verify(password, row["password_hash"]):
        return None

    return {
        "id": row["id"],
        "email": row["email"],
        "full_name": row["full_name"],
        "role": row["role"],
        "created_at": row["created_at"],
    }


def create_access_token(user_id: str, role: str) -> str:
    """Create a JWT access token."""
    payload = {
        "sub": user_id,
        "role": role,
        "type": "access",
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def create_refresh_token(user_id: str) -> str:
    """Create a JWT refresh token."""
    payload = {
        "sub": user_id,
        "type": "refresh",
        "exp": datetime.datetime.now(datetime.timezone.utc)
        + datetime.timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS),
    }
    return jwt.encode(payload, SECRET_KEY, algorithm=JWT_ALGORITHM)


def decode_token(token: str) -> dict | None:
    """Decode and validate a JWT token. Returns payload or None."""
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[JWT_ALGORITHM])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None


def get_user_by_id(user_id: str) -> dict | None:
    """Fetch user by ID."""
    conn = get_connection()
    row = conn.execute(
        "SELECT id, email, full_name, role, created_at FROM users WHERE id = ?",
        (user_id,),
    ).fetchone()
    conn.close()

    if not row:
        return None

    return dict(row)
