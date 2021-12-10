from sqlalchemy.orm import Session
from typing import List

from . import models, schemas


# region User
def get_user_by_login(db: Session, login: str):
    return db.query(models.User).filter(models.User.email == login).first()


def create_user(db: Session, new_user: schemas.UserRegister):
    new_user_db = models.User(**new_user.dict())
    db.add(new_user_db)
    db.commit()
    db.refresh(new_user_db)
    return


def update_user_bu_id(db: Session, id: int, user_data: schemas.UserUpdate):
    _ = db.query(models.User).filter(models.User.id == id)\
        .update(user_data.dict())
    db.commit()
    return
# endregion


# region Room
def read_rooms(db: Session):
    return db.query(models.Room).all()


def create_room(db: Session, room_data: schemas.RoomData):
    room_db = models.Room(**room_data.dict())
    db.add(room_db)
    db.commit()
    db.refresh(room_db)
    return


def update_room_by_id(db: Session, id: int, room_data: schemas.RoomData):
    _ = db.query(models.Room).filter(models.Room.id == id)\
        .update(room_data.dict())
    db.commit()
    return


def add_room_options(db: Session, id: int, options: List[int]):
    room_options = [models.RoomOption(room_id=id, option_id=option_id)
                    for option_id in options]
    db.add_all(room_options)
    db.commit()
    return


def remove_room_options(db: Session, id: int, options: List[int]):
    _ = db.query(models.RoomOption).filter(models.RoomOption.room_id == id)\
        .delete()
    db.commit()
    return
# endregion


# region Option
def create_option(db: Session, option_data: schemas.OptionData):
    option_db = models.Option(**option_data.dict())
    db.add(option_db)
    db.commit()
    db.refresh(option_db)
    return


def read_options(db: Session):
    return db.query(models.Option).all()
# endregion
