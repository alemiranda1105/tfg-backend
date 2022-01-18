from fastapi import APIRouter, Response, status

from app.server.controllers import method_controller

router = APIRouter(
    prefix="/methods",
    tags=["methods"]
)


@router.get("/all")
async def get_all_methods(response: Response):
    methods = await method_controller.find_all()
    if len(methods) <= 0:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "error": "No hemos encontrado ningún resultado"
        }
    return methods
