from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List


# region Users
class UserBase(BaseModel):
    email: str
    is_admin: bool = False


class UserUpdate(BaseModel):
    first_name: Optional[str]
    second_name: Optional[str]
    phone_number: Optional[str]


class UserRegister(UserBase):
    password: str


class UserData(UserBase, UserUpdate):
    pass


class User(UserData):
    id: int
    password: str

    class Config:
        orm_mode = True
# endregion


# region Options
class OptionData(BaseModel):
    cost: int
    name: str


class Option(OptionData):
    id: int

    class Config:
        orm_mode = True
# endregion


# region Room
class RoomData(BaseModel):
    name: str
    description: Optional[str]
    cost: int
    start: int
    finish: int
    image_id: Optional[int]


class Room(RoomData):
    id: int
    options: Optional[List[Option]]

    class Config:
        orm_mode = True
# endregion


# region Reservation
class ReservationCreate(BaseModel):
    cost: int
    start: datetime
    finish: datetime
    user_id: int = None
    email: str
    first_name: str = ''
    second_name: str = ''
    phone_number: str = ''


class ReservationData(ReservationCreate):
    room_id: int


class Reservation(ReservationData):
    id: int
    options: List[Option]

    class Config:
        orm_mode = True
# endregion


# region Token
class Token(BaseModel):
    access_token: str
    token_type: str
# endregion
