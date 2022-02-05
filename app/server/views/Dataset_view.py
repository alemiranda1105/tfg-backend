from fastapi import APIRouter
from fastapi.responses import FileResponse

from app.server.controllers.Dataset_controller import get_dataset_file

router = APIRouter(
    prefix="/dataset",
    tags=["dataset"]
)


@router.get("/")
async def download_dataset():
    file = get_dataset_file()
    return FileResponse(file)
