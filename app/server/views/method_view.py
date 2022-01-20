from fastapi import APIRouter, Response, status

from app.server.controllers.method_controller import find_all, find_by_id
from app.server.models.CustomResponse import error_response

router = APIRouter(
    prefix="/methods",
    tags=["methods"]
)


@router.get("/all")
async def get_all_methods(response: Response):
    methods = await find_all()
    if len(methods) <= 0:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No hemos encontrado ningún resultado")
    return methods


@router.get("/{method_id}")
async def get_method_by_id(method_id: str, response: Response):
    if len(method_id) < 24:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response("No ha sido posible completar la operación")
    method = await find_by_id(method_id)
    if not method:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No hemos encontrado ningún resultado")
    else:
        return method
