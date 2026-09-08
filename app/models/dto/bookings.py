from datetime import datetime

from pydantic import BaseModel, Field


class CreateBookingRequest(BaseModel):
    room_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime
    purpose: str = Field(min_length=1)


class ExtendBookingRequest(BaseModel):
    end_time: datetime


class BookingResponse(BaseModel):
    id: int
    room_id: int
    user_id: int
    start_time: datetime
    end_time: datetime
    purpose: str


class BookingListResponse(BaseModel):
    bookings: list[BookingResponse]