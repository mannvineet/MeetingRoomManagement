import asyncio

from pwdlib import PasswordHash

from app.helpers.security import create_access_token
from app.repositories.user_repository import UserRepository


class AuthService:

    password_hash = PasswordHash.recommended()

    def __init__(self, repository: UserRepository):
        self.repository = repository

    @staticmethod
    def hash_password(password: str):
        return AuthService.password_hash.hash(password)

    @staticmethod
    def verify_password(password: str, hashed_password: str):
        return AuthService.password_hash.verify(
            password,
            hashed_password
        )

    async def login(self, email: str, password: str):
        user = await self.repository.get_by_email(email)

        if user is None:
            return None

        valid_password = self.verify_password(
            password,
            user.hashed_password
        )

        if not valid_password:
            return None

        token = create_access_token(
            user.id,
            user.role
        )

        return token