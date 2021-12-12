from fastapi import APIRouter, Depends, Response
from sqlalchemy.orm import Session

from ..database import crud
from ..dependencies import get_db
from ..utils import auth


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.post("/init/", status_code=201, summary="Load initial data")
async def load_initial_data(
    current_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    _ = crud.load_init_data(db=db)
    return Response(status_code=201)
