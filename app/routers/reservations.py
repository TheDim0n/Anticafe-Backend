from fastapi import APIRouter, Depends, Response
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth


router = APIRouter(prefix="/reservations", tags=["Reservations"])


@router.get("/", response_model=List[schemas.Reservation])
async def read_reservations(
    current_user=Depends(auth.get_current_user),
    db=Depends(get_db)
):
    user_id = None
    if not current_user.is_admin:
        user_id = current_user.id
    return crud.get_reservations(db=db, user_id=user_id)


@router.delete("/{id}/", status_code=204)
async def remove_reservation(
    id: int,
    db=Depends(get_db)
):
    _ = crud.remove_reservation_by_id(db=db, id=id)
    return Response(status_code=204)
