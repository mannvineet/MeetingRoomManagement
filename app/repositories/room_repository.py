from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db.rooms import Rooms


class RoomRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, room: Rooms):
        self.db.add(room)
        await self.db.commit()
        return room

    async def get_by_id(self, room_id: int):
        result = await self.db.execute(
            select(Rooms).where(Rooms.id == room_id)
        )
        return result.scalars().first()

    async def get_by_number(self, number: int):
        result = await self.db.execute(
            select(Rooms).where(Rooms.number == number)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(
            select(Rooms)
        )
        return result.scalars().all()

    async def update(self, room: Rooms):
        await self.db.commit()
        return room

    async def delete(self, room: Rooms):
        await self.db.delete(room)
        await self.db.commit()
