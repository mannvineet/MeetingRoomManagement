from contextlib import asynccontextmanager

from fastapi import FastAPI, HTTPException
from fastapi.exceptions import RequestValidationError

from app.helpers.database import Base, engine

from app.exception_handlers import (
    handle_http_exception,
    handle_validation_error
)

from app.models.db.users import Users
from app.models.db.rooms import Rooms
from app.models.db.bookings import Bookings

from app.helpers.all_routers import include_routers


@asynccontextmanager
async def lifespan(app: FastAPI):
    async with engine.begin() as connection:
        await connection.run_sync(
            Base.metadata.create_all
        )

    yield

    await engine.dispose()


app = FastAPI(
    title="Meeting Room Management System",
    lifespan=lifespan
)

app.add_exception_handler(
    HTTPException,
    handle_http_exception
)

app.add_exception_handler(
    RequestValidationError,
    handle_validation_error
)

include_routers(app)