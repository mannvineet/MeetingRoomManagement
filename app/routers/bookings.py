from fastapi import APIRouter, Depends, status

from app.core.dependencies import get_booking_service,get_current_user,require_admin

from app.models.users import Users
from app.schemas.bookings import CreateBookingRequest,ExtendBookingRequest
from app.schemas.response import APIResponse
from app.services.booking_service import BookingService


router = APIRouter(
    prefix="/bookings",
    tags=["Bookings"]
)


@router.post("",status_code=status.HTTP_201_CREATED,response_model=APIResponse)
async def create_booking(data: CreateBookingRequest,service: BookingService = Depends(get_booking_service),
    current_user: Users = Depends(get_current_user)):
    booking = await service.create_booking(data,current_user)

    return {
        "success": True,
        "message": "Booking created successfully",
        "data": {
            "id": booking.id,
            "room_id": booking.room_id,
            "user_id": booking.user_id,
            "start_time": booking.start_time,
            "end_time": booking.end_time,
            "purpose": booking.purpose
        },
        "errors": []
    }


@router.get("/me",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def get_my_bookings(service: BookingService = Depends(get_booking_service),
    current_user: Users = Depends(get_current_user)):

    bookings = await service.get_my_bookings(current_user.id)

    return {
        "success": True,
        "message": "Bookings retrieved successfully",
        "data": {
            "bookings": [
                {
                    "id": booking.id,
                    "room_id": booking.room_id,
                    "user_id": booking.user_id,
                    "start_time": booking.start_time,
                    "end_time": booking.end_time,
                    "purpose": booking.purpose
                }
                for booking in bookings
            ]
        },
        "errors": []
    }


@router.get("",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def get_all_bookings(service: BookingService = Depends(get_booking_service),
    current_user: Users = Depends(require_admin)):

    bookings = await service.get_all_bookings()

    return {
        "success": True,
        "message": "Bookings retrieved successfully",
        "data": {
            "bookings": [
                {
                    "id": booking.id,
                    "room_id": booking.room_id,
                    "user_id": booking.user_id,
                    "start_time": booking.start_time,
                    "end_time": booking.end_time,
                    "purpose": booking.purpose
                }
                for booking in bookings
            ]
        },
        "errors": []
    }


@router.patch("/{booking_id}/extend",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def extend_booking(booking_id: int,data: ExtendBookingRequest,service: BookingService = Depends(get_booking_service),
    current_user: Users = Depends(get_current_user)):

    booking = await service.extend_booking(booking_id,data,current_user)

    return {
        "success": True,
        "message": "Booking extended successfully",
        "data": {
            "id": booking.id,
            "room_id": booking.room_id,
            "user_id": booking.user_id,
            "start_time": booking.start_time,
            "end_time": booking.end_time,
            "purpose": booking.purpose
        },
        "errors": []
    }


@router.delete("/{booking_id}",status_code=status.HTTP_200_OK,response_model=APIResponse)
async def cancel_booking(booking_id: int,service: BookingService = Depends(get_booking_service),
    current_user: Users = Depends(get_current_user)):

    await service.cancel_booking(booking_id,current_user)

    return {
        "success": True,
        "message": "Booking cancelled successfully",
        "data": {},
        "errors": []
    }