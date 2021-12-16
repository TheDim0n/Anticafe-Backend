from datetime import datetime, timedelta

from sqlalchemy import func as sql_func
from sqlalchemy.orm import Session
from sqlalchemy.sql import expression as sql_exp
from typing import List

from . import models, schemas
from ..utils import files


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
                options: List[int] = [], id: int = None):
    if not id:
        id = db.query(sql_func.max(models.Room.id)).first()[0] + 1
    room_db = models.Room(id=id, **room_data.dict())
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
    _ = db.query(models.RoomOption).filter(
        models.RoomOption.room_id == id,
        models.RoomOption.option_id.in_(options)
    ).delete()
    db.commit()
    return
# endregion


# region Option
def create_option(db: Session, option_data: schemas.OptionData):
    id = db.query(sql_func.max(models.Option.id)).first()[0] + 1
    option_db = models.Option(id=id, **option_data.dict())
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
    _ = db.query(models.ReservationOption).filter_by(reservation_id=id)\
        .delete()
    db.commit()
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


# region Info
def read_project_info(db: Session):
    return db.query(models.Info).first()


def update_project_info(db: Session, info: schemas.Info):
    _ = db.query(models.Info).update(info.dict())
    db.commit()
    return
# endregion


# region InitData
def load_init_data(db: Session):
    options = files.json_loader("app/database/init_data/options.json")
    for option in options:
        option_db = db.query(models.Option)\
            .filter(models.Option.id == option["id"]).first()
        if not option_db:
            option_db = models.Option(**option)
            db.add(option_db)
    db.commit()

    rooms = files.json_loader("app/database/init_data/rooms.json")
    for room in rooms:
        room_db = db.query(models.Room).filter_by(id=room["id"]).first()
        if not room_db:
            room_data = schemas.RoomData(**room["room_data"])
            options = room["options"]
            _ = create_room(db=db, room_data=room_data,
                            options=options, id=room["id"])

    info = files.json_loader("app/database/init_data/info.json")
    info_db = read_project_info(db=db)
    if info_db:
        update_project_info(db=db, info=schemas.Info(**info))
    else:
        info_db = models.Info(**info)
        db.add(info_db)
        db.commit()
        db.refresh(info_db)

    return
# endregion


# region Statistic
def get_statistics(db: Session):
    today = datetime.now().replace(
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )

    total_reservations = sql_func.count(models.Reservation.id)\
        .label("total_reservations")
    total_cost = sql_func.sum(models.Reservation.cost).label("total_cost")
    total_hours = sql_func.sum(
        (models.Reservation.finish - models.Reservation.start)
    ).label("total_hours")

    query = db.query(
        models.Reservation.room_id,
        models.Room.name,
        total_reservations,
        total_cost,
        total_hours
    ).join(models.Room).filter(
        models.Reservation.start >= today - timedelta(days=30),
        models.Reservation.finish < today,
    ).group_by(models.Room.name, models.Reservation.room_id).order_by(
        total_reservations.desc(),
        total_cost.desc(),
        total_hours.desc(),
    )

    data_id = [row["room_id"] for row in query.all()]
    additional_query = db.query(
        models.Room.id.label("room_id"),
        models.Room.name,
        sql_exp.literal(0).label("total_reservations"),
        sql_exp.literal(0).label("total_cost"),
        sql_exp.literal(timedelta(hours=0)).label("total_hours"),
    ).filter(models.Room.id.not_in(data_id))
    header = ["room_id", "name", "total_reservations", "total_cost",
              "total_hours"]
    return query.all(), additional_query.all(), header
# endregion
