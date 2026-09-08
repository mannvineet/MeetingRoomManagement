from pydantic import BaseModel, Field


class CreateRoomRequest(BaseModel):
    number: int = Field(gt=0)
    capacity: int = Field(gt=0)


class UpdateRoomRequest(BaseModel):
    number: int | None = Field(default=None, gt=0)
    capacity: int | None = Field(default=None, gt=0)
    status: str | None = Field(default=None, min_length=1)


class RoomResponse(BaseModel):
    id: int
    number: int
    capacity: int
    status: str


class RoomListResponse(BaseModel):
    rooms: list[RoomResponse]