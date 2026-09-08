from fastapi import FastAPI

from app.routers.auth import router as auth_router
from app.routers.users import router as users_router
from app.routers.rooms import router as rooms_router
from app.routers.bookings import router as bookings_router


routers = [auth_router,users_router,rooms_router,bookings_router]


def include_routers(app: FastAPI):
    for router in routers:
        app.include_router(router,prefix="/api/v1")