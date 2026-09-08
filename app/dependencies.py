from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session

from app.database import get_db
from app.core.security import decode_token
from app.models.users import Users

from app.repositories.user_repository import UserRepository
from app.repositories.room_repository import RoomRepository
from app.repositories.booking_repository import BookingRepository

from app.services.auth_service import AuthService
from app.services.user_service import UserService
from app.services.room_service import RoomService
from app.services.booking_service import BookingService


oauth2_bearer = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/token"
)


db_dependency = Annotated[Session,Depends(get_db)]


def get_user_repository(db: db_dependency):
    return UserRepository(db)


def get_user_service(repository=Depends(get_user_repository)):
    return UserService(repository)


def get_room_repository(db: db_dependency):
    return RoomRepository(db)


def get_room_service(
    repository=Depends(get_room_repository)
):
    return RoomService(repository)


def get_booking_repository(db: db_dependency):
    return BookingRepository(db)


def get_booking_service(
    booking_repository=Depends(get_booking_repository),
    room_repository=Depends(get_room_repository)
):
    return BookingService(
        booking_repository,
        room_repository
    )


def get_auth_service(
    repository=Depends(get_user_repository)
):
    return AuthService(repository)


def get_current_user(token: Annotated[str, Depends(oauth2_bearer)],repository=Depends(get_user_repository)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid authentication credentials"
    )

    try:
        payload = decode_token(token)

        user_id = payload.get("id")

        if user_id is None:
            raise credentials_exception

        user_id = int(user_id)

    except (JWTError, ValueError):
        raise credentials_exception

    user = repository.get_by_id(user_id)

    if user is None:
        raise credentials_exception

    return user


def require_admin(current_user: Users = Depends(get_current_user)):
    if current_user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )

    return current_user