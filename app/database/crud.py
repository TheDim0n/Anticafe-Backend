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


def create_room(db: Session, room_data: schemas.RoomData,
                options: List[int] = []):
    room_db = models.Room(**room_data.dict())
    for option_id in options:
        option_db = db.query(models.Option)\
            .filter(models.Option.id == option_id).first()
        room_db.options.append(option_db)
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


# region Reservation
def get_reservations(db: Session, user_id: int = None):
    query = db.query(models.Reservation)
    if user_id:
        query = query.filter(models.Reservation.user_id == user_id)
    return query.all()


def get_reservations_by_room(db: Session, id: int, start=None, finish=None):
    query = db.query(models.Reservation).\
        filter(models.Reservation.room_id == id)
    if start:
        query = query.filter(
            models.Reservation.start >= start,
            models.Reservation.finish <= finish,
        )
    return query.all()


def remove_reservation_by_id(db: Session, id: int):
    _ = db.query(models.Reservation).filter(models.Reservation.id == id).\
        delete()
    db.commit()
    return


def create_resevation_for_room(db: Session,
                               reservation: schemas.ReservationData,
                               options: List[int] = []):
    db_reservation = models.Reservation(**reservation.dict())
    for option_id in options:
        option_db = db.query(models.Option)\
            .filter(models.Option.id == option_id).first()
        db_reservation.options.append(option_db)
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return
# endregion
