from datetime import datetime
from unittest.mock import Mock, AsyncMock

import pytest
from fastapi import HTTPException

from app.services.booking_service import BookingService


class TestBookingService:

    def setup_method(self):
        self.booking_repository = Mock()
        self.room_repository = Mock()

        self.booking_repository.get_overlapping = AsyncMock()
        self.booking_repository.create = AsyncMock()
        self.room_repository.get_by_id = AsyncMock()

        self.service = BookingService(
            self.booking_repository,
            self.room_repository
        )

    @pytest.mark.asyncio
    async def test_create_booking_success(self):
        data = Mock()
        data.room_id = 1
        data.start_time = datetime(2026, 9, 10, 10, 0)
        data.end_time = datetime(2026, 9, 10, 11, 0)
        data.purpose = "Team meeting"

        room = Mock()
        room.status = "AVAILABLE"

        booking = Mock()

        self.room_repository.get_by_id.return_value = room
        self.booking_repository.get_overlapping.return_value = None
        self.booking_repository.create.return_value = booking

        result = await self.service.create_booking(data, 10)

        assert result == booking

        self.room_repository.get_by_id.assert_awaited_once_with(1)
        self.booking_repository.get_overlapping.assert_awaited_once_with(
            1,
            data.start_time,
            data.end_time
        )
        self.booking_repository.create.assert_awaited_once()


    @pytest.mark.asyncio
    async def test_create_booking_room_not_found(self):
        data = Mock()
        data.room_id = 1
        data.start_time = datetime(2026, 9, 10, 10, 0)
        data.end_time = datetime(2026, 9, 10, 11, 0)
        data.purpose = "Team meeting"

        self.room_repository.get_by_id.return_value = None

        with pytest.raises(HTTPException) as exc:
            await self.service.create_booking(data, 10)

        assert exc.value.status_code == 404
        assert exc.value.detail == "Room not found"

        self.room_repository.get_by_id.assert_awaited_once_with(1)

        self.booking_repository.get_overlapping.assert_not_awaited()
        self.booking_repository.create.assert_not_awaited()