import io
import json
from typing import Optional, List

from fastapi import APIRouter, Body, Depends, File, HTTPException
from fastapi.encoders import jsonable_encoder
from starlette.responses import StreamingResponse

from app.server.auth.auth_bearer import JWTBearer
from app.server.controllers.Method_controller import find_all, find_by_id, create_method, find_by_user_id, \
    update_method, delete_method, download_all_methods, update_and_evaluate
from app.server.models.CustomResponse import ErrorResponse
from app.server.models.Method import MethodSchema

router = APIRouter(
    prefix="/methods",
    tags=["methods"]
)


@router.get("/all",
            responses={
                200: {"model": MethodSchema},
                404: {"model": ErrorResponse}
            })
async def get_all_methods():
    methods = find_all()
    if len(methods) <= 0:
        raise HTTPException(404, "No hemos encontrado ningún resultado")
    return methods


@router.get("/user_methods",
            responses={
                200: {"model": List[MethodSchema]},
                400: {"model": ErrorResponse},
                500: {"model": ErrorResponse}
            },
            dependencies=[Depends(JWTBearer())])
async def get_method_by_user_id(user_id: str = None):
    if user_id is None:
        raise HTTPException(400, "Error al buscar los metodos del usuario")
    methods = find_by_user_id(user_id)
    if not methods:
        raise HTTPException(500, "No se ha encontrado ningún resultado para este usuario")
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


@router.get("/{method_id}",
            responses={
                200: {"model": MethodSchema},
                400: {"model": ErrorResponse},
                404: {"model": ErrorResponse}
            })
async def get_method_by_id(method_id: str):
    if len(method_id) != 24:
        raise HTTPException(400, "No ha sido posible completar la operación")
    method = find_by_id(method_id)
    if not method:
        raise HTTPException(404, "No se ha podido encontrar este método")
    else:
        return method


@router.post("/",
             status_code=201,
             responses={
                 201: {"model": MethodSchema},
                 500: {"model": ErrorResponse}
             },
             dependencies=[Depends(JWTBearer())])
async def upload_method(file: bytes = File(...), data: str = Body(...)):
    data_json = json.loads(data)
    data = jsonable_encoder(data_json)
    file = io.BytesIO(file)
    new_method = create_method(data, file)
    if not new_method:
        raise HTTPException(500, "No se ha podido completar la solicitud")
    return new_method


@router.put("/{method_id}",
            responses={
                200: {"model": MethodSchema},
                422: {"model": ErrorResponse}
            },
            dependencies=[Depends(JWTBearer())])
async def modify_method(method_id: str, file: Optional[bytes] = File(None), data: str = Body(...)):
    data_json = json.loads(data)
    data = jsonable_encoder(data_json)
    if file is not None:
        file = io.BytesIO(file)
        updated = update_and_evaluate(method_id, data, file)
    else:
        updated = update_method(method_id, data)
    if not updated:
        raise HTTPException(422, "No se ha podido completar la acción")
    return updated


@router.delete("/{method_id}",
               responses={
                   404: {"model": ErrorResponse}
               },
               dependencies=[Depends(JWTBearer())])
async def remove_method(method_id: str):
    removed = delete_method(method_id)
    if not removed:
        raise HTTPException(404, "No ha sido posible completar la actualización")
    return {"success": True}
