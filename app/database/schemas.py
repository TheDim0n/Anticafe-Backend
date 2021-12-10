from pydantic import BaseModel
from typing import Optional


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


# region Token
class Token(BaseModel):
    access_token: str
    token_type: str
# endregion