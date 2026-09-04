from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.bookings import Bookings


class BookingRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, booking: Bookings):
        self.db.add(booking)
        await self.db.flush()
        return booking

    async def get_by_id(self, booking_id: int):
        result = await self.db.execute(
            select(Bookings).where(
                Bookings.id == booking_id
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(Bookings).order_by(Bookings.id)
        )

        return result.scalars().all()

    async def get_by_user(self, user_id: int):
        result = await self.db.execute(
            select(Bookings)
            .where(Bookings.user_id == user_id)
            .order_by(Bookings.start_time)
        )

        return result.scalars().all()

    async def delete(self, booking: Bookings):
        await self.db.delete(booking)