from pydantic import BaseModel, EmailStr, Field

from app.models.user_role import UserRole


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: UserRole
    password: str = Field(min_length=6, max_length=128)


class UpdateUserRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    role: UserRole | None = None


class UserResponse(BaseModel):
    id: int = Field(gt=0)
    name: str = Field(min_length=1, max_length=100)
    email: EmailStr
    role: UserRole


class UserListResponse(BaseModel):
    users: list[UserResponse]