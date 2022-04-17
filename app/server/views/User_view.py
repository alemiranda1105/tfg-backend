from fastapi import APIRouter, Body, HTTPException, Depends, Request
from fastapi.encoders import jsonable_encoder

from app.server.auth.auth_bearer import JWTBearer
from app.server.auth.auth_handler import get_id_from_token
from app.server.controllers.Method_controller import delete_by_user_id
from app.server.controllers.User_controller import create_user, verify_user, find_user_by_id, get_user_profile, \
    update_user, delete_user
from app.server.models.CustomResponse import ErrorResponse
from app.server.models.User import BaseUserSchema, NewUserSchema, LoginUserSchema

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/profile",
            responses={
                200: {"model": BaseUserSchema},
                403: {"model": ErrorResponse},
                404: {"model": ErrorResponse}
            },
            dependencies=[Depends(JWTBearer())])
async def show_user_profile(user_id: str, request: Request):
    token_id = ""
    if 'authorization' in request.headers:
        try:
            token_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            token_id = ""

    # Check if the user trying to watch the profile is the same
    if token_id != user_id:
        raise HTTPException(403, "User not valid")

    user = get_user_profile(user_id)
    if not user:
        raise HTTPException(404, "We could not find the user")
    return user


@router.get("/{user_id}",
            responses={
                200: {"model": BaseUserSchema},
                404: {"model": ErrorResponse}
            })
async def show_user(user_id: str):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "We could not find the user")
    return user


@router.post("/login",
             responses={
                 200: {"model": BaseUserSchema},
                 404: {"model": ErrorResponse}
             })
async def login(user_data: LoginUserSchema = Body(...)):
    user = jsonable_encoder(user_data)
    current_user = await verify_user(user)
    if not current_user:
        raise HTTPException(404, "Wrong data")
    return current_user


@router.post("/",
             status_code=201,
             responses={
                 201: {"model": BaseUserSchema},
                 422: {"model": ErrorResponse}
             })
async def sign_up(user_data: NewUserSchema = Body(...)):
    user = jsonable_encoder(user_data)
    new_user = await create_user(user)
    if not new_user:
        raise HTTPException(422, "We could not create the user")
    return new_user


@router.put("/{user_id}",
            status_code=200,
            responses={
                200: {"model": BaseUserSchema},
                403: {"model": ErrorResponse},
                500: {"model": ErrorResponse}
            },
            dependencies=[Depends(JWTBearer())])
async def modify_user(user_id: str, request: Request, data: BaseUserSchema = Body(...)):
    token_id = ""
    if 'authorization' in request.headers:
        try:
            token_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            raise HTTPException(403, "Not valid token")

    # Check if the user trying to watch the profile is the same
    if token_id != user_id:
        raise HTTPException(403, "User not valid")

    data = jsonable_encoder(data)
    if 'id' in data:
        del data['id']

    updated = update_user(user_id, data)
    if not updated:
        raise HTTPException(500, "The user was not updated")
    return updated


@router.delete("/{user_id}", dependencies=[Depends(JWTBearer())])
async def remove_user(user_id: str, request: Request):
    token_id = ""
    if 'authorization' in request.headers:
        try:
            token_id = get_id_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            raise HTTPException(403, "Not valid token")

    # Check if the user trying to delete the profile is the same
    if token_id != user_id:
        raise HTTPException(403, "Wrong user")

    methods_removed = delete_by_user_id(user_id, token_id)
    if methods_removed:
        removed = delete_user(user_id)
        if removed:
            return {"result": True}
    raise HTTPException(500, "We could not complete the operation")
