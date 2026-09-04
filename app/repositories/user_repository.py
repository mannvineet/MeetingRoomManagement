from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.users import Users


class UserRepository:

    def __init__(self, db: AsyncSession):
        self.db = db

    async def create(self, user: Users):
        self.db.add(user)
        await self.db.flush()
        return user

    async def get_by_id(self, user_id: int):
        result = await self.db.execute(
            select(Users).where(
                Users.id == user_id
            )
        )

        return result.scalar_one_or_none()

    async def get_by_email(self, email: str):
        result = await self.db.execute(
            select(Users).where(
                Users.email == email
            )
        )

        return result.scalar_one_or_none()

    async def get_all(self):
        result = await self.db.execute(
            select(Users).order_by(Users.id)
        )

        return result.scalars().all()

    async def delete(self, user: Users):
        await self.db.delete(user)