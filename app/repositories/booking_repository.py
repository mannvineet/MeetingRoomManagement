from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db.bookings import Bookings


class BookingRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, booking: Bookings):
        self.db.add(booking)
        await self.db.commit()
        return booking

    async def get_by_id(self, booking_id: int):
        result = await self.db.execute(
            select(Bookings).where(Bookings.id == booking_id)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(
            select(Bookings)
        )
        return result.scalars().all()

    async def get_by_user(self, user_id: int):
        result = await self.db.execute(
            select(Bookings).where(
                Bookings.user_id == user_id
            )
        )
        return result.scalars().all()

    async def get_overlapping(
        self,
        room_id,
        start_time,
        end_time,
        exclude_booking_id=None
    ):
        query = select(Bookings).where(
            Bookings.room_id == room_id,
            Bookings.start_time < end_time,
            Bookings.end_time > start_time
        )

        if exclude_booking_id is not None:
            query = query.where(
                Bookings.id != exclude_booking_id
            )

        result = await self.db.execute(query)
        return result.scalars().first()

    async def update(self, booking: Bookings):
        await self.db.commit()
        return booking

    async def delete(self, booking: Bookings):
        await self.db.delete(booking)
        await self.db.commit()
