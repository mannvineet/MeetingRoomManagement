from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from app.models.bookings import Bookings
from app.models.users import Users
from app.repositories.booking_repository import BookingRepository
from app.repositories.room_repository import RoomRepository
from app.schemas.bookings import (
    CreateBookingRequest,
    ExtendBookingRequest
)


class BookingService:

    def __init__(self,booking_repository: BookingRepository,room_repository: RoomRepository):
        self.booking_repository = booking_repository
        self.room_repository = room_repository

    async def create_booking(self,data: CreateBookingRequest,current_user: Users):

        room = await self.room_repository.get_by_id(data.room_id)

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        if room.status != "ACTIVE":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Room is not available"
            )

        if data.end_time <= data.start_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="End time must be after start time"
            )

        booking = Bookings(
            room_id=data.room_id,
            user_id=current_user.id,
            start_time=data.start_time,
            end_time=data.end_time,
            purpose=data.purpose
        )

        try:
            await self.booking_repository.create(booking)
            await self.booking_repository.db.commit()
            await self.booking_repository.db.refresh(booking)

        except IntegrityError as exc:
            await self.booking_repository.db.rollback()

            if "no_overlapping_room_booking" in str(exc):
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Room is already booked for this time"
                )

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Could not create booking"
            )

        return booking

    async def get_my_bookings(self,current_user: Users):

        return await self.booking_repository.get_by_user(current_user.id)

    async def get_all_bookings(self):
        return await self.booking_repository.get_all()

    async def extend_booking(self,booking_id: int,data: ExtendBookingRequest,current_user: Users):
        booking = await self.booking_repository.get_by_id(booking_id)

        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        if (booking.user_id != current_user.id and current_user.role != "ADMIN"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot modify this booking"
            )

        if data.end_time <= booking.end_time:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="New end time must be after current end time"
            )

        booking.end_time = data.end_time

        try:
            await self.booking_repository.db.commit()
            await self.booking_repository.db.refresh(booking)

        except IntegrityError:
            await self.booking_repository.db.rollback()
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room is already booked for the extended time"
            )

        return booking

    async def cancel_booking(self,booking_id: int,current_user: Users):
        booking = await self.booking_repository.get_by_id(booking_id)

        if booking is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Booking not found"
            )

        if (booking.user_id != current_user.id and current_user.role != "ADMIN"):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You cannot cancel this booking"
            )

        await self.booking_repository.delete(booking)
        await self.booking_repository.db.commit()