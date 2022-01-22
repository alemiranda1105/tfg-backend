from fastapi import APIRouter, Response, status, Body
from fastapi.encoders import jsonable_encoder

from app.server.controllers.User_controller import create_user, verify_user
from app.server.models.CustomResponse import error_response
from app.server.models.User import UserSchema, UserLoginSchema

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/login")
async def login(response: Response, user_data: UserLoginSchema = Body(...)):
    user = jsonable_encoder(user_data)
    current_user = await verify_user(user)
    if not current_user:
        response.status_code = status.HTTP_404_NOT_FOUND
        return error_response("Compruebe los datos e inténtelo de nuevo")
    return current_user


@router.post("/", status_code=201)
async def sign_up(response: Response, user_data: UserSchema = Body(...)):
    user = jsonable_encoder(user_data)
    new_user = await create_user(user)
    if not new_user:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return error_response("No se ha podido crear al usuario")
    return new_user
