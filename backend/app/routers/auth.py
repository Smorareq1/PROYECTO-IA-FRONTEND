from fastapi import APIRouter, Depends, HTTPException

from app.dependencies import get_current_user
from app.models.auth import LoginRequest, RefreshRequest, AuthResponse, UserResponse
from app.services.auth_service import (
    authenticate_user,
    create_access_token,
    create_refresh_token,
    decode_token,
    get_user_by_id,
)

router = APIRouter()


@router.post("/login", response_model=AuthResponse)
def login(body: LoginRequest):
    user = authenticate_user(body.email, body.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid email or password")

    access_token = create_access_token(user["id"], user["role"])
    refresh_token = create_refresh_token(user["id"])

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "user": user,
    }


@router.post("/refresh")
def refresh(body: RefreshRequest):
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    user = get_user_by_id(payload["sub"])
    if not user:
        raise HTTPException(status_code=401, detail="User not found")

    access_token = create_access_token(user["id"], user["role"])
    return {"access_token": access_token}


@router.post("/logout", status_code=204)
def logout(user: dict = Depends(get_current_user)):
    # Stateless JWT — nothing to invalidate server-side
    return None


@router.get("/me", response_model=UserResponse)
def me(user: dict = Depends(get_current_user)):
    return user
