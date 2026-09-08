from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.db.users import Users


class UserRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: Users):
        self.db.add(user)
        await self.db.commit()
        return user

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(Users).where(Users.id == user_id)
        )
        return result.scalars().first()

    async def get_by_email(self, email: str):
        result = await self.db.execute(
            select(Users).where(Users.email == email)
        )
        return result.scalars().first()

    async def get_all(self):
        result = await self.db.execute(
            select(Users)
        )
        return result.scalars().all()

    async def update(self, user: Users):
        await self.db.commit()
        return user

    async def delete(self, user: Users):
        await self.db.delete(user)
        await self.db.commit()
