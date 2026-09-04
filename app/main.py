from contextlib import asynccontextmanager

from fastapi import FastAPI,HTTPException
from fastapi.exceptions import RequestValidationError

from app.core.exception_handlers import (
    handle_http_exception,
    handle_validation_error
)

from app.db.base import Base
from app.db.connection import engine

from app.models import Users, Rooms, Bookings

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.rooms import router as rooms_router
from app.routers.bookings import router as bookings_router


@asynccontextmanager
async def lifespan(app: FastAPI):

    async with engine.begin() as connection:
        await connection.run_sync(Base.metadata.create_all)

    yield

    await engine.dispose()


app = FastAPI(
    title="Meeting Room Management System",
    lifespan=lifespan
)

app.add_exception_handler(HTTPException,handle_http_exception)
app.add_exception_handler(RequestValidationError,handle_validation_error)

app.include_router(
    auth_router,
    prefix="/api/v1"
)

app.include_router(
    users_router,
    prefix="/api/v1"
)

app.include_router(
    rooms_router,
    prefix="/api/v1"
)

app.include_router(
    bookings_router,
    prefix="/api/v1"
)