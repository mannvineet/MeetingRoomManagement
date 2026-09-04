from pydantic import BaseModel


class CreateRoomRequest(BaseModel):
    number: int
    capacity: int


class UpdateRoomRequest(BaseModel):
    number: int | None = None
    capacity: int | None = None
    status: str | None = None


class RoomResponse(BaseModel):
    id: int
    number: int
    capacity: int
    status: str

    model_config = {
        "from_attributes": True
    }