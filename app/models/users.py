from sqlalchemy import Column, Integer, String

from app.db.base import Base


class Users(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    role = Column(String, nullable=False, default="USER")
    hashed_password = Column(String, nullable=False)