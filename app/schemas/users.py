from pydantic import BaseModel


class CreateUserRequest(BaseModel):
    name: str
    email: str
    role: str
    password: str


class UpdateUserRequest(BaseModel):
    name: str | None = None
    role: str | None = None


class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str

    model_config = {
        "from_attributes": True
    }