from fastapi import APIRouter, Depends

from app.dependencies import (
    get_current_user,
    get_room_service,
    require_admin
)
from app.models.dto.response import APIResponse
from app.models.dto.rooms import (
    CreateRoomRequest,
    UpdateRoomRequest,
    RoomListResponse,
    RoomResponse
)
from app.services.room_service import RoomService


router = APIRouter(prefix="/rooms", tags=["Rooms"])


@router.post("", response_model=APIResponse)
async def create_room(
    data: CreateRoomRequest,
    service: RoomService = Depends(get_room_service),
    current_user=Depends(require_admin)
):
    room = await service.create_room(data)

    return APIResponse(
        success=True,
        message="Room created successfully",
        data=RoomResponse(
            id=room.id,
            number=room.number,
            capacity=room.capacity,
            status=room.status
        )
    )


@router.get("", response_model=APIResponse)
async def get_rooms(
    service: RoomService = Depends(get_room_service),
    current_user=Depends(get_current_user)
):
    rooms = await service.get_rooms()

    return APIResponse(
        success=True,
        message="Rooms fetched successfully",
        data=RoomListResponse(
            rooms=[
                RoomResponse(
                    id=room.id,
                    number=room.number,
                    capacity=room.capacity,
                    status=room.status
                )
                for room in rooms
            ]
        )
    )


@router.get("/{room_id}", response_model=APIResponse)
async def get_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    current_user=Depends(get_current_user)
):
    room = await service.get_room(room_id)

    return APIResponse(
        success=True,
        message="Room fetched successfully",
        data=RoomResponse(
            id=room.id,
            number=room.number,
            capacity=room.capacity,
            status=room.status
        )
    )


@router.put("/{room_id}", response_model=APIResponse)
async def update_room(
    room_id: int,
    data: UpdateRoomRequest,
    service: RoomService = Depends(get_room_service),
    current_user=Depends(require_admin)
):
    room = await service.update_room(room_id, data)

    return APIResponse(
        success=True,
        message="Room updated successfully",
        data=RoomResponse(
            id=room.id,
            number=room.number,
            capacity=room.capacity,
            status=room.status
        )
    )


@router.delete("/{room_id}", response_model=APIResponse)
async def delete_room(
    room_id: int,
    service: RoomService = Depends(get_room_service),
    current_user=Depends(require_admin)
):
    await service.delete_room(room_id)

    return APIResponse(
        success=True,
        message="Room deleted successfully",
        data=None
    )
