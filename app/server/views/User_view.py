from fastapi import APIRouter, Response, status, Body
from fastapi.encoders import jsonable_encoder

from app.server.controllers.User_controller import create_user
from app.server.models.CustomResponse import error_response
from app.server.models.User import UserSchema

router = APIRouter(
    prefix="/users",
    tags=["users"]
)


@router.post("/", status_code=201)
async def sign_up(response: Response, user_data: UserSchema = Body(...)):
    user = jsonable_encoder(user_data)
    new_user = await create_user(user)
    if not new_user:
        response.status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
        return error_response("No se ha podido crear al usuario")
    return new_user
