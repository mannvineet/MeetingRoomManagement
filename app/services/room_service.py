from fastapi import HTTPException

from app.models.room_status import RoomStatus
from app.models.db.rooms import Rooms


class RoomService:
    def __init__(self, repository):
        self.repository = repository

    async def create_room(self, data):
        if data.number <= 0:
            raise HTTPException(
                400,
                "Room number must be greater than 0"
            )

        if data.capacity <= 0:
            raise HTTPException(
                400,
                "Capacity must be greater than 0"
            )

        if await self.repository.get_by_number(data.number):
            raise HTTPException(
                409,
                "Room number already exists"
            )

        room = Rooms(
            number=data.number,
            capacity=data.capacity,
            status=RoomStatus.ACTIVE.value
        )

        return await self.repository.create(room)

    async def get_rooms(self):
        return await self.repository.get_all()

    async def get_room(self, room_id: int):
        room = await self.repository.get_by_id(room_id)

        if room is None:
            raise HTTPException(404, "Room not found")

        return room

    async def update_room(self, room_id: int, data):
        room = await self.get_room(room_id)

        if data.number is not None:
            if data.number <= 0:
                raise HTTPException(
                    400,
                    "Room number must be greater than 0"
                )

            existing_room = await self.repository.get_by_number(
                data.number
            )

            if existing_room and existing_room.id != room.id:
                raise HTTPException(
                    409,
                    "Room number already exists"
                )

            room.number = data.number

        if data.capacity is not None:
            if data.capacity <= 0:
                raise HTTPException(
                    400,
                    "Capacity must be greater than 0"
                )

            room.capacity = data.capacity

        if data.status is not None:
            if data.status not in [
                status.value for status in RoomStatus
            ]:
                raise HTTPException(
                    400,
                    "Invalid room status"
                )

            room.status = data.status

        return await self.repository.update(room)

    async def delete_room(self, room_id: int):
        room = await self.get_room(room_id)
        await self.repository.delete(room)
