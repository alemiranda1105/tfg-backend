from fastapi import APIRouter, Response, status, Body
from fastapi.encoders import jsonable_encoder

from app.server.controllers.method_controller import find_all, find_by_id, create_method, find_by_user_id
from app.server.models.CustomResponse import error_response
from app.server.models.method import MethodSchema

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


@router.get("/user_methods")
async def get_method_by_user_id(response: Response, user_id: str = None):
    if user_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response("Error al buscar los metodos del usuario")
    print(user_id)
    methods = await find_by_user_id(user_id)
    if not methods:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No se ha encontrado ningún resultado para este usuario")
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


@router.post("/")
async def upload_method(response: Response, data: MethodSchema = Body(...)):
    data = jsonable_encoder(data)
    new_method = await create_method(data)
    if not new_method:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No se ha podido subir el método")
    response.status_code = status.HTTP_201_CREATED
    return new_method
