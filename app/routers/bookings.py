from fastapi import APIRouter, Depends

from app.dependencies import get_booking_service, get_current_user
from app.models.dto.bookings import (
    BookingListResponse,
    BookingResponse,
    CreateBookingRequest,
    ExtendBookingRequest
)
from app.models.dto.response import APIResponse
from app.services.booking_service import BookingService


router = APIRouter(prefix="/bookings", tags=["Bookings"])


@router.post("", response_model=APIResponse)
async def create_booking(
    data: CreateBookingRequest,
    service: BookingService = Depends(get_booking_service),
    current_user=Depends(get_current_user)
):
    booking = await service.create_booking(
        data,
        current_user.id
    )

    return APIResponse(
        success=True,
        message="Booking created successfully",
        data=BookingResponse(
            id=booking.id,
            room_id=booking.room_id,
            user_id=booking.user_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
            purpose=booking.purpose
        )
    )


@router.get("", response_model=APIResponse)
async def get_bookings(
    service: BookingService = Depends(get_booking_service),
    current_user=Depends(get_current_user)
):
    bookings = await service.get_bookings()

    return APIResponse(
        success=True,
        message="Bookings fetched successfully",
        data=BookingListResponse(
            bookings=[
                BookingResponse(
                    id=booking.id,
                    room_id=booking.room_id,
                    user_id=booking.user_id,
                    start_time=booking.start_time,
                    end_time=booking.end_time,
                    purpose=booking.purpose
                )
                for booking in bookings
            ]
        )
    )


@router.get("/my", response_model=APIResponse)
async def get_my_bookings(
    service: BookingService = Depends(get_booking_service),
    current_user=Depends(get_current_user)
):
    bookings = await service.get_my_bookings(
        current_user.id
    )

    return APIResponse(
        success=True,
        message="My bookings fetched successfully",
        data=BookingListResponse(
            bookings=[
                BookingResponse(
                    id=booking.id,
                    room_id=booking.room_id,
                    user_id=booking.user_id,
                    start_time=booking.start_time,
                    end_time=booking.end_time,
                    purpose=booking.purpose
                )
                for booking in bookings
            ]
        )
    )


@router.get("/{booking_id}", response_model=APIResponse)
async def get_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
    current_user=Depends(get_current_user)
):
    booking = await service.get_booking(booking_id)

    return APIResponse(
        success=True,
        message="Booking fetched successfully",
        data=BookingResponse(
            id=booking.id,
            room_id=booking.room_id,
            user_id=booking.user_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
            purpose=booking.purpose
        )
    )


@router.put("/{booking_id}/extend", response_model=APIResponse)
async def extend_booking(
    booking_id: int,
    data: ExtendBookingRequest,
    service: BookingService = Depends(get_booking_service),
    current_user=Depends(get_current_user)
):
    booking = await service.extend_booking(
        booking_id,
        data.end_time,
        current_user
    )

    return APIResponse(
        success=True,
        message="Booking extended successfully",
        data=BookingResponse(
            id=booking.id,
            room_id=booking.room_id,
            user_id=booking.user_id,
            start_time=booking.start_time,
            end_time=booking.end_time,
            purpose=booking.purpose
        )
    )


@router.delete("/{booking_id}", response_model=APIResponse)
async def cancel_booking(
    booking_id: int,
    service: BookingService = Depends(get_booking_service),
    current_user=Depends(get_current_user)
):
    await service.cancel_booking(
        booking_id,
        current_user
    )

    return APIResponse(
        success=True,
        message="Booking cancelled successfully",
        data=None
    )
