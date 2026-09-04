from sqlalchemy import CheckConstraint,Column,DateTime,ForeignKey,Integer,String,func
from sqlalchemy.dialects.postgresql import ExcludeConstraint

from app.db.base import Base


class Bookings(Base):
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer,ForeignKey("rooms.id"),nullable=False)
    user_id = Column(Integer,ForeignKey("users.id"),nullable=False)
    start_time = Column(DateTime(timezone=True),nullable=False)
    end_time = Column(DateTime(timezone=True),nullable=False)
    purpose = Column(String,nullable=False)

    __table_args__ = (
        CheckConstraint("end_time > start_time",name="valid_booking_time"),
        ExcludeConstraint(("room_id", "="),
            (
                func.tstzrange(
                    start_time,
                    end_time,
                    "[)"
                ),
                "&&"
            ),
            name="no_overlapping_room_booking",
            using="gist"
        ),
    )