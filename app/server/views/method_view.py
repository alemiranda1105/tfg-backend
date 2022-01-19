from fastapi import APIRouter, Response, status

from app.server.controllers.method_controller import find_all, find_by_id

router = APIRouter(
    prefix="/methods",
    tags=["methods"]
)


@router.get("/all")
async def get_all_methods(response: Response):
    methods = await find_all()
    if len(methods) <= 0:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "error": "No hemos encontrado ningún resultado"
        }
    return methods


@router.get("/{method_id}")
async def get_method_by_id(method_id: str, response: Response):
    if len(method_id) < 24:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return {
            "error": "No ha sido posible completar la operación"
        }
    method = await find_by_id(method_id)
    if method is None:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return {
            "error": "No hemos encontrado ningún resultado"
        }
    else:
        return method
