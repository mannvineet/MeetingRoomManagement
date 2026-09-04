from fastapi import HTTPException, status

from app.models.rooms import Rooms
from app.repositories.room_repository import RoomRepository
from app.schemas.rooms import (
    CreateRoomRequest,
    UpdateRoomRequest
)


class RoomService:

    def __init__(self, repository: RoomRepository):
        self.repository = repository

    async def create_room(self,data: CreateRoomRequest):
        existing_room = await self.repository.get_by_number(data.number)

        if existing_room:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Room number already exists"
            )

        if data.capacity <= 0:
            raise HTTPException(
                status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                detail="Capacity must be greater than 0"
            )

        room = Rooms(
            number=data.number,
            capacity=data.capacity,
            status="ACTIVE"
        )

        await self.repository.create(room)
        await self.repository.db.commit()
        await self.repository.db.refresh(room)

        return room

    async def get_all_rooms(self):
        return await self.repository.get_all()

    async def get_room(self, room_id: int):
        room = await self.repository.get_by_id(room_id)

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        return room

    async def update_room(self,room_id: int,data: UpdateRoomRequest):
        room = await self.repository.get_by_id(room_id)

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        if data.number is not None:
            existing_room = await self.repository.get_by_number(data.number)

            if existing_room and existing_room.id != room.id:
                raise HTTPException(
                    status_code=status.HTTP_409_CONFLICT,
                    detail="Room number already exists"
                )

            room.number = data.number

        if data.capacity is not None:
            if data.capacity <= 0:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Capacity must be greater than 0"
                )

            room.capacity = data.capacity

        if data.status is not None:
            allowed_statuses = ["ACTIVE","INACTIVE","MAINTENANCE"]

            if data.status not in allowed_statuses:
                raise HTTPException(
                    status_code=status.HTTP_422_UNPROCESSABLE_CONTENT,
                    detail="Invalid room status"
                )

            room.status = data.status

        await self.repository.db.commit()
        await self.repository.db.refresh(room)

        return room

    async def delete_room(self, room_id: int):
        room = await self.repository.get_by_id(room_id)

        if room is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Room not found"
            )

        await self.repository.delete(room)
        await self.repository.db.commit()