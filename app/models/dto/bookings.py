from datetime import datetime

from pydantic import BaseModel, Field


class CreateBookingRequest(BaseModel):
    room_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime
    purpose: str = Field(min_length=1, max_length=255)


class ExtendBookingRequest(BaseModel):
    end_time: datetime


class BookingResponse(BaseModel):
    id: int = Field(gt=0)
    room_id: int = Field(gt=0)
    user_id: int = Field(gt=0)
    start_time: datetime
    end_time: datetime
    purpose: str = Field(min_length=1, max_length=255)


class BookingListResponse(BaseModel):
    bookings: list[BookingResponse]