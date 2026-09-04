from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.rooms import Rooms


class RoomRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, room: Rooms):
        self.db.add(room)
        await self.db.flush()
        return room

    async def get_by_id(self, room_id: int):
        result = await self.db.execute(
            select(Rooms).where(
                Rooms.id == room_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_number(self, number: int):
        result = await self.db.execute(
            select(Rooms).where(
                Rooms.number == number
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(Rooms).order_by(Rooms.id)
        )

        return result.scalars().all()

    async def delete(self, room: Rooms):
        await self.db.delete(room)