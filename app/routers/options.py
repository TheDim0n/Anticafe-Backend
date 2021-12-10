from fastapi import APIRouter, Depends, Response
from typing import List

from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth


router = APIRouter(prefix="/options", tags=["Options"])


@router.get("/", response_model=List[schemas.Option])
async def read_options(db=Depends(get_db)):
    return crud.read_options(db=db)


@router.post("/", status_code=201)
async def create_option(
    option_data: schemas.OptionData,
    current_user=Depends(auth.get_current_admin),
    db=Depends(get_db)
):
    _ = crud.create_option(db=db, option_data=option_data)
    return Response(status_code=201)
