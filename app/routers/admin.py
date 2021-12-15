from fastapi import APIRouter, Depends, HTTPException, Response
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session
from starlette.background import BackgroundTask

from ..database import crud, schemas
from ..dependencies import get_db
from ..utils import auth, files


router = APIRouter(
    prefix="/admin",
    tags=["Admin"]
)


@router.get("/info/", response_model=schemas.Info, summary="Read project info")
async def read_project_info(db: Session = Depends(get_db)):
    return crud.read_project_info(db=db)


@router.patch("/info/", status_code=204, summary="Update project info")
async def update_project_info(
    info: schemas.Info,
    current_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    _ = crud.update_project_info(db=db, info=info)
    return Response(status_code=204)


@router.post("/init/", status_code=201, summary="Load initial data")
async def load_initial_data(
    current_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    _ = crud.load_init_data(db=db)
    return Response(status_code=201)


@router.get("/statistics/")
async def get_statistics(
    # current_user=Depends(auth.get_current_admin),
    db: Session = Depends(get_db)
):
    data, header = crud.get_statistics(db=db)
    if not data:
        raise HTTPException(status_code=404, detail="Reservations not found")
    outcsv = files.data_to_csv(header=header, data=data)
    return FileResponse(
        outcsv.name, media_type="text/csv", filename="Statistics.csv",
        background=BackgroundTask(files.delete_file, filepath=outcsv.name)
    )
