from fastapi import APIRouter, Body, HTTPException
from fastapi.encoders import jsonable_encoder

from app.server.controllers.User_controller import create_user, verify_user, find_user_by_id
from app.server.models.CustomResponse import ErrorResponse
from app.server.models.User import UserSchema, UserLoginSchema, LoggedUserSchema, ExternalUserSchema

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.get("/{user_id}",
            responses={
                200: {"model": ExternalUserSchema},
                404: {"model": ErrorResponse}
            })
async def show_user(user_id: str):
    user = find_user_by_id(user_id)
    if not user:
        raise HTTPException(404, "No se pudo encontrar al usuario")
    return user


@router.post("/login",
             responses={
                 200: {"model": LoggedUserSchema},
                 404: {"model": ErrorResponse}
             })
async def login(user_data: UserLoginSchema = Body(...)):
    user = jsonable_encoder(user_data)
    current_user = await verify_user(user)
    if not current_user:
        raise HTTPException(404, "Usuario/Contraseña incorrectos")
    return current_user


@router.post("/",
             status_code=201,
             responses={
                 201: {"model": LoggedUserSchema},
                 422: {"model": ErrorResponse}
             })
async def sign_up(user_data: UserSchema = Body(...)):
    user = jsonable_encoder(user_data)
    new_user = await create_user(user)
    if not new_user:
        raise HTTPException(422, "No se ha podido crear al usuario")
    return new_user
