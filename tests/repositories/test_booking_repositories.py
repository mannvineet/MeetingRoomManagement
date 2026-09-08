from unittest.mock import Mock, AsyncMock

import pytest

from app.repositories.booking_repository import BookingRepository


class TestBookingRepository:

    def setup_method(self):
        self.db = Mock()
        self.db.add = Mock()
        self.db.commit = AsyncMock()

        self.repository = BookingRepository(self.db)

    @pytest.mark.asyncio
    async def test_create_booking_success(self):
        booking = Mock()

        result = await self.repository.create(booking)

        assert result == booking

        self.db.add.assert_called_once_with(booking)
        self.db.commit.assert_awaited_once()