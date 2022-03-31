import io
import json
from typing import Optional, List

from fastapi import APIRouter, Body, Depends, File, HTTPException, Request
from fastapi.encoders import jsonable_encoder
from starlette.responses import StreamingResponse

from app.server.auth.auth_bearer import JWTBearer
from app.server.auth.auth_handler import get_id_from_token
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
async def get_all_methods(request: Request):
    user_id = ""
    if 'authorization' in request.headers:
        try:
            user_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            user_id = ""
    methods = find_all(user_id)
    if len(methods) <= 0:
        raise HTTPException(404, "We could not find any method")
    return methods


@router.get("/user_methods",
            responses={
                200: {"model": List[MethodSchema]},
                400: {"model": ErrorResponse},
                404: {"model": ErrorResponse}
            },
            dependencies=[Depends(JWTBearer())])
async def get_method_by_user_id(request: Request, user_id: str = None):
    if user_id is None:
        raise HTTPException(400, "The user is not valid")
    token_id = ""
    if 'authorization' in request.headers:
        try:
            token_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            token_id = ""
    methods = find_by_user_id(user_id, token_id)
    if not methods:
        raise HTTPException(404, "We could not find any method")
    return methods


@router.get("/download_csv", response_class=StreamingResponse)
async def download_csv(request: Request):
    user_id = ""
    if 'authorization' in request.headers:
        try:
            user_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            user_id = ""
    file = download_all_methods("csv", user_id)
    if not file:
        raise HTTPException(503, "We could not complete the request")
    response = StreamingResponse(iter([file.getvalue()]), media_type="text/csv")
    response.headers["Content-Disposition"] = "attachment; filename=results.csv"
    return response


@router.get("/download_xls", response_class=StreamingResponse)
async def download_xls(request: Request):
    user_id = ""
    if 'authorization' in request.headers:
        try:
            user_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            user_id = ""
    file = download_all_methods("xls", user_id)
    if not file:
        raise HTTPException(503, "We could not complete the request")
    response = StreamingResponse(iter([file.getvalue()]), media_type="application/vnd.ms-excel")
    response.headers["Content-Disposition"] = "attachment; filename=results.xlsx"
    return response


@router.get("/download_json")
async def download_json(request: Request):
    user_id = ""
    if 'authorization' in request.headers:
        try:
            user_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            user_id = ""
    file = download_all_methods("json", user_id)
    if not file:
        raise HTTPException(503, "We could not complete the request")
    return file


@router.get("/{method_id}",
            responses={
                200: {"model": MethodSchema},
                400: {"model": ErrorResponse},
                404: {"model": ErrorResponse}
            })
async def get_method_by_id(method_id: str, request: Request):
    if len(method_id) != 24:
        raise HTTPException(400, "The operation was not completed")
    user_id = ""
    if 'authorization' in request.headers:
        try:
            user_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            user_id = ""
    method = find_by_id(method_id, user_id)
    if not method:
        raise HTTPException(404, "Method not found")
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
async def modify_method(method_id: str, request: Request, file: Optional[bytes] = File(None), data: str = Body(...)):
    data_json = json.loads(data)
    data = jsonable_encoder(data_json)

    if 'authorization' in request.headers:
        try:
            user_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            raise HTTPException(403, 'Not valid token')
    else:
        raise HTTPException(403, 'Not valid token')

    if 'id' in data:
        del data['id']
    if file is not None:
        file = io.BytesIO(file)
        updated = update_and_evaluate(method_id, data, file, user_id)
    else:
        updated = update_method(method_id, data, user_id)
    if not updated:
        raise HTTPException(422, "The method was not updated")
    return updated


@router.delete("/{method_id}",
               responses={
                   404: {"model": ErrorResponse}
               },
               dependencies=[Depends(JWTBearer())])
async def remove_method(method_id: str, request: Request):
    if 'authorization' in request.headers:
        try:
            user_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            raise HTTPException(403, 'Not valid token')
    else:
        raise HTTPException(403, 'Not valid token')

    removed = delete_method(method_id, user_id)
    if not removed:
        raise HTTPException(404, "The method was not delete")
    return {"success": True}
