from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth


router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)


@router.get("/", summary="Read list of rooms",
            response_model=List[schemas.Room])
async def read_rooms(db: Session = Depends(get_db)):
    return crud.read_rooms(db=db)


@router.post("/", summary="Create new room", status_code=201)
async def create_room(
    room_data: schemas.RoomData,
    current_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    _ = crud.create_room(db, room_data)
    return Response(status_code=201)


@router.patch("/{id}/", summary="Update room data by id")
async def update_room_data(
    id: int,
    room_data: schemas.RoomData,
    create_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    _ = crud.update_room_by_id(db=db, id=id, room_data=room_data)
    return Response(status_code=204)


@router.post("/{id}/options/", status_code=201,
             summary="Add options from room")
async def add_room_options(
    id: int,
    options: List[int],
    create_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    _ = crud.add_room_options(db=db, id=id, options=options)
    return Response(status_code=201)


@router.delete("/{id}/options/", status_code=204,
               summary="Remove options from room")
async def remove_room_options(
    id: int,
    options: List[int],
    create_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    _ = crud.remove_room_options(db=db, id=id, options=options)
    return Response(status_code=204)