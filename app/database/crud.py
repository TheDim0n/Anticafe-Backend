from sqlalchemy.orm import Session

from . import models, schemas


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
