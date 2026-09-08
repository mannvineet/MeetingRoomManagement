from pydantic import BaseModel, EmailStr, Field


class CreateUserRequest(BaseModel):
    name: str = Field(min_length=1)
    email: EmailStr
    role: str = Field(min_length=1)
    password: str = Field(min_length=6)


class UpdateUserRequest(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    role: str | None = Field(default=None, min_length=1)


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str


class UserListResponse(BaseModel):
    users: list[UserResponse]