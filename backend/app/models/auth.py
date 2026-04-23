from pydantic import BaseModel


class LoginRequest(BaseModel):
    email: str
    password: str


class RefreshRequest(BaseModel):
    refresh_token: str


class UserResponse(BaseModel):
    id: str
    email: str
    full_name: str
    role: str
    created_at: str


class AuthResponse(BaseModel):
    access_token: str
    refresh_token: str
    user: UserResponse
