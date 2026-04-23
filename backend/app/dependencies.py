"""
Shared FastAPI dependencies (auth, model access).
"""
from fastapi import Depends, HTTPException, Header

from app.services.auth_service import decode_token, get_user_by_id


def get_current_user(authorization: str | None = Header(None)) -> dict:
    """Extract and validate the current user from the Authorization header."""
    if not authorization or not authorization.startswith("Bearer "):
        raise HTTPException(status_code=401, detail="Missing or invalid authorization header")

    token = authorization.split(" ", 1)[1]
    payload = decode_token(token)

    if not payload or payload.get("type") != "access":
        raise HTTPException(status_code=401, detail="Invalid or expired token")

    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    return user


def require_role(*roles: str):
    """Dependency factory: require the current user to have one of the given roles."""
    def check(user: dict = Depends(get_current_user)):
        if user["role"] not in roles:
            raise HTTPException(status_code=403, detail="Insufficient permissions")
        return user
    return check
