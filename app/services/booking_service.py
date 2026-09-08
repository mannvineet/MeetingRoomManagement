from fastapi import HTTPException

from app.models.room_status import RoomStatus
from app.models.db.bookings import Bookings


class BookingService:
    def __init__(
        self,
        booking_repository,
        room_repository
    ):
        self.booking_repository = booking_repository
        self.room_repository = room_repository

    async def create_booking(self, data, user_id):
        if data.room_id <= 0:
            raise HTTPException(
                400,
                "Invalid room id"
            )

        if not data.purpose.strip():
            raise HTTPException(
                400,
                "Purpose is required"
            )

        if data.end_time <= data.start_time:
            raise HTTPException(
                400,
                "End time must be greater than start time"
            )

        room = await self.room_repository.get_by_id(data.room_id)

        if room is None:
            raise HTTPException(
                404,
                "Room not found"
            )

        if room.status != RoomStatus.AVAILABLE.value:
            raise HTTPException(
                400,
                "Room is not active"
            )

        overlapping = await self.booking_repository.get_overlapping(
            data.room_id,
            data.start_time,
            data.end_time
        )

        if overlapping:
            raise HTTPException(
                409,
                "Room is already booked for this time"
            )

        booking = Bookings(
            room_id=data.room_id,
            user_id=user_id,
            start_time=data.start_time,
            end_time=data.end_time,
            purpose=data.purpose
        )

        return await self.booking_repository.create(booking)

    async def get_bookings(self):
        return await self.booking_repository.get_all()

    async def get_booking(self, booking_id):
        booking = await self.booking_repository.get_by_id(
            booking_id
        )

        if booking is None:
            raise HTTPException(
                404,
                "Booking not found"
            )

        return booking

    async def get_my_bookings(self, user_id):
        return await self.booking_repository.get_by_user(
            user_id
        )

    async def extend_booking(
        self,
        booking_id,
        new_end_time,
        current_user
    ):
        booking = await self.get_booking(booking_id)

        if (
            booking.user_id != current_user.id
            and current_user.role != "ADMIN"
        ):
            raise HTTPException(
                403,
                "You cannot modify this booking"
            )

        if new_end_time <= booking.end_time:
            raise HTTPException(
                400,
                "New end time must be greater than current end time"
            )

        overlapping = await self.booking_repository.get_overlapping(
            booking.room_id,
            booking.start_time,
            new_end_time,
            booking.id
        )

        if overlapping:
            raise HTTPException(
                409,
                "Room is already booked for this time"
            )

        booking.end_time = new_end_time

        return await self.booking_repository.update(booking)

    async def cancel_booking(
        self,
        booking_id,
        current_user
    ):
        booking = await self.get_booking(booking_id)

        if (
            booking.user_id != current_user.id
            and current_user.role != "ADMIN"
        ):
            raise HTTPException(
                403,
                "You cannot cancel this booking"
            )

        await self.booking_repository.delete(booking)
