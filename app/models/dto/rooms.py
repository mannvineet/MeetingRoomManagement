from pydantic import BaseModel, Field

from app.models.room_status import RoomStatus


class CreateRoomRequest(BaseModel):
    number: int = Field(gt=0)
    capacity: int = Field(gt=0)


class UpdateRoomRequest(BaseModel):
    number: int | None = Field(default=None, gt=0)
    capacity: int | None = Field(default=None, gt=0)
    status: RoomStatus | None = None


class RoomResponse(BaseModel):
    id: int = Field(gt=0)
    number: int = Field(gt=0)
    capacity: int = Field(gt=0)
    status: RoomStatus


class RoomListResponse(BaseModel):
    rooms: list[RoomResponse]