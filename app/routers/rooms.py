from fastapi import APIRouter, Depends, status

from app.core.dependencies import (
    get_room_service,
    get_current_user,
    require_admin
)
from app.models.users import Users
from app.schemas.response import APIResponse
from app.schemas.rooms import (
    CreateRoomRequest,
    UpdateRoomRequest
)
from app.services.room_service import RoomService


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.post("",status_code=status.HTTP_201_CREATED,response_model=APIResponse)
async def create_room(data: CreateRoomRequest,service: RoomService = Depends(get_room_service),
    current_user: Users = Depends(require_admin)):

    room = await service.create_room(data)

    return {
        "success": True,
        "message": "Room created successfully",
        "data": {
            "id": room.id,
            "number": room.number,
            "capacity": room.capacity,
            "status": room.status
        },
        "errors": []
    }


@router.get("",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def get_rooms(service: RoomService = Depends(get_room_service),
    current_user: Users = Depends(get_current_user)):

    rooms = await service.get_all_rooms()

    return {
        "success": True,
        "message": "Rooms retrieved successfully",
        "data": {
            "rooms": [
                {
                    "id": room.id,
                    "number": room.number,
                    "capacity": room.capacity,
                    "status": room.status
                }
                for room in rooms
            ]
        },
        "errors": []
    }


@router.get("/{room_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def get_room(room_id: int,service: RoomService = Depends(get_room_service),
    current_user: Users = Depends(get_current_user)):

    room = await service.get_room(room_id)

    return {
        "success": True,
        "message": "Room retrieved successfully",
        "data": {
            "id": room.id,
            "number": room.number,
            "capacity": room.capacity,
            "status": room.status
        },
        "errors": []
    }


@router.patch("/{room_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def update_room(room_id: int,data: UpdateRoomRequest,service: RoomService = Depends(get_room_service),
    current_user: Users = Depends(require_admin)):

    room = await service.update_room(room_id, data)

    return {
        "success": True,
        "message": "Room updated successfully",
        "data": {
            "id": room.id,
            "number": room.number,
            "capacity": room.capacity,
            "status": room.status
        },
        "errors": []
    }


@router.delete("/{room_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def delete_room(room_id: int,service: RoomService = Depends(get_room_service),
    current_user: Users = Depends(require_admin)):

    await service.delete_room(room_id)

    return {
        "success": True,
        "message": "Room deleted successfully",
        "data": {},
        "errors": []
    }