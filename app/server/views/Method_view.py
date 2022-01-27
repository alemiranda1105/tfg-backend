import io
import json
from typing import Optional, List

from fastapi import APIRouter, Response, status, Body, Depends, File
from fastapi.encoders import jsonable_encoder
from starlette.responses import StreamingResponse

from app.server.auth.auth_bearer import JWTBearer
from app.server.controllers.Method_controller import find_all, find_by_id, create_method, find_by_user_id, \
    update_method, delete_method, download_all_methods, update_and_evaluate
from app.server.models.CustomResponse import error_response
from app.server.models.Method import MethodSchema

router = APIRouter(
    prefix="/methods",
    tags=["methods"]
)


@router.get("/all", response_model=List[MethodSchema])
async def get_all_methods(response: Response):
    methods = find_all()
    if len(methods) <= 0:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No hemos encontrado ningún resultado")
    return methods


@router.get("/user_methods", response_model=List[MethodSchema], dependencies=[Depends(JWTBearer())])
async def get_method_by_user_id(response: Response, user_id: str = None):
    if user_id is None:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response("Error al buscar los metodos del usuario")
    methods = find_by_user_id(user_id)
    if not methods:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No se ha encontrado ningún resultado para este usuario")
    return methods


@router.get("/download_csv", response_class=StreamingResponse)
async def download_csv():
    file = download_all_methods("csv")
    response = StreamingResponse(iter([file.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=results.csv"
    return response


@router.get("/download_xls", response_class=StreamingResponse)
async def download_xls():
    file = download_all_methods("xls")
    response = StreamingResponse(iter([file.getvalue()]), media_type="application/vnd.ms-excel")
    response.headers["Content-Disposition"] = "attachment; filename=results.xlsx"
    return response


@router.get("/download_json")
async def download_json():
    file = download_all_methods("json")
    return file


@router.get("/{method_id}", response_model=MethodSchema)
async def get_method_by_id(method_id: str, response: Response):
    if len(method_id) < 24:
        response.status_code = status.HTTP_400_BAD_REQUEST
        return error_response("No ha sido posible completar la operación")
    method = find_by_id(method_id)
    if not method:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No hemos encontrado ningún resultado")
    else:
        return method


@router.post("/", response_model=MethodSchema, dependencies=[Depends(JWTBearer())])
async def upload_method(response: Response, file: bytes = File(...), data: str = Body(...)):
    data_json = json.loads(data)
    data = jsonable_encoder(data_json)
    file = io.BytesIO(file)
    new_method = create_method(data, file)
    if not new_method:
        response.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        return error_response("No se ha podido subir el método")
    response.status_code = status.HTTP_201_CREATED
    return new_method


@router.put("/{method_id}", response_model=MethodSchema, dependencies=[Depends(JWTBearer())])
async def modify_method(response: Response, method_id: str, file: Optional[bytes] = File(None), data: str = Body(...)):
    data_json = json.loads(data)
    data = jsonable_encoder(data_json)
    if file is not None:
        file = io.BytesIO(file)
        updated = update_and_evaluate(method_id, data, file)
    else:
        updated = update_method(method_id, data)
    if not updated:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return error_response("No ha sido posible completar la operación")
    return updated


@router.delete("/{method_id}", dependencies=[Depends(JWTBearer())])
async def remove_method(response: Response, method_id: str):
    removed = delete_method(method_id)
    if not removed:
        response.status_code = status.HTTP_404_NOT_FOUND
        return error_response("No ha sido posible completar la operación")
    return {"success": True}
