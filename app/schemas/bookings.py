from datetime import datetime

from pydantic import BaseModel


class CreateBookingRequest(BaseModel):
    room_id: int
    start_time: datetime
    end_time: datetime
    purpose: str


class ExtendBookingRequest(BaseModel):
    end_time: datetime


class BookingResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    purpose: str

    model_config = {
        "from_attributes": True
    }