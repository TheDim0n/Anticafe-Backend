from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from .database import DataBase


class User(DataBase):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    email = Column(String(64), nullable=False)
    password = Column(String(255), nullable=False)
    is_admin = Column(Boolean(), nullable=False, default=False)
    first_name = Column(String(25), nullable=True)
    second_name = Column(String(25), nullable=True)
    phone_number = Column(String(12), nullable=True)


class Room(DataBase):
    __tablename__ = "room"

    id = Column(Integer, primary_key=True)
    name = Column(String(30), nullable=False)
    description = Column(String, nullable=True)
    cost = Column(Integer, nullable=False)
    start = Column(Integer, nullable=False)
    finish = Column(Integer, nullable=False)
    image_id = Column(Integer, nullable=True)

    options = relationship("Option", secondary="room_option")


class Reservation(DataBase):
    __tablename__ = "reservation"

    id = Column(Integer, primary_key=True)
    cost = Column(Integer, nullable=False)
    start = Column(DateTime, nullable=False)
    finish = Column(DateTime, nullable=False)
    room_id = Column(Integer, ForeignKey("room.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    email = Column(String(64), nullable=False)
    first_name = Column(String(25), nullable=True)
    second_name = Column(String(25), nullable=True)
    phone_number = Column(String(12), nullable=True)


class Option(DataBase):
    __tablename__ = "option"

    id = Column(Integer, primary_key=True)
    cost = Column(Integer, nullable=False)
    name = Column(String(30), nullable=False)


class RoomOption(DataBase):
    __tablename__ = "room_option"

    room_id = Column(Integer, ForeignKey("room.id"), primary_key=True)
    option_id = Column(Integer, ForeignKey("option.id"), primary_key=True)


class ReservationOption(DataBase):
    __tablename__ = "reservation_option"

    reservation_id = Column(Integer,
                            ForeignKey("reservation.id"), primary_key=True)
    option_id = Column(Integer, ForeignKey("option.id"), primary_key=True)
