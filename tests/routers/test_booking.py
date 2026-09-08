from datetime import datetime, timezone
from unittest.mock import Mock, AsyncMock

from fastapi import FastAPI
from fastapi.testclient import TestClient

from app.routers.bookings import router
from app.dependencies import get_booking_service, get_current_user


class TestBookingRouter:

    def setup_method(self):
        self.app = FastAPI()
        self.app.include_router(router, prefix="/api/v1")

        self.service = Mock()
        self.service.create_booking = AsyncMock()

        self.current_user = Mock()
        self.current_user.id = 10

        self.app.dependency_overrides[get_booking_service] = (
            lambda: self.service
        )

        self.app.dependency_overrides[get_current_user] = (
            lambda: self.current_user
        )

        self.client = TestClient(self.app)

    def teardown_method(self):
        self.app.dependency_overrides.clear()

    def test_create_booking_success(self):
        booking = Mock()

        booking.id = 1
        booking.room_id = 2
        booking.user_id = 10
        booking.start_time = datetime(
            2026, 9, 10, 10, 0, tzinfo=timezone.utc
        )
        booking.end_time = datetime(
            2026, 9, 10, 11, 0, tzinfo=timezone.utc
        )
        booking.purpose = "Team meeting"

        self.service.create_booking.return_value = booking

        response = self.client.post(
            "/api/v1/bookings",
            json={
                "room_id": 2,
                "start_time": "2026-09-10T10:00:00Z",
                "end_time": "2026-09-10T11:00:00Z",
                "purpose": "Team meeting"
            }
        )

        assert response.status_code == 200

        body = response.json()

        assert body["success"] is True
        assert body["message"] == "Booking created successfully"

        assert body["data"]["id"] == 1
        assert body["data"]["room_id"] == 2
        assert body["data"]["user_id"] == 10
        assert body["data"]["purpose"] == "Team meeting"

        self.service.create_booking.assert_awaited_once()