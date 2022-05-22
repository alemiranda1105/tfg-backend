from typing import List

from fastapi import APIRouter, HTTPException, Body, Request, Depends
from fastapi.encoders import jsonable_encoder

from server.auth.auth_bearer import JWTBearer
from server.auth.auth_handler import get_role_from_token
from server.controllers.Content_controller import get_all_content, get_content_by_title, get_content_by_id, create_content, \
    update_content, delete_content, get_content_by_page
from server.models.Content import ContentSchema, NewContentSchema
from server.models.CustomResponse import ErrorResponse

router = APIRouter(
    prefix="/content",
    tags=["content"]
)


@router.get("/page/{page}",
            responses={
                200: {"model": ContentSchema},
                404: {"model": ErrorResponse}
            })
async def show_content_by_id(page: str):
    content = get_content_by_page(page)
    if not content:
        raise HTTPException(404, "We could not find any content")
    return content


@router.get("/by_id/{content_id}",
            responses={
                200: {"model": ContentSchema},
                404: {"model": ErrorResponse}
            })
async def show_content_by_id(content_id: str):
    content = get_content_by_id(content_id)
    if not content:
        raise HTTPException(404, "We could not find any content")
    return content


@router.get("/{title}",
            responses={
                200: {"model": ContentSchema},
                404: {"model": ErrorResponse}
            })
async def show_content_by_title(title: str):
    content = get_content_by_title(title)
    if not content:
        raise HTTPException(404, "We could not find any content")
    return content


@router.get("/",
            responses={
                200: {"model": List[ContentSchema]},
                404: {"model": ErrorResponse}
            })
async def show_all_content():
    content = get_all_content()
    if len(content) <= 0:
        raise HTTPException(404, "We could not find any content")
    return content


@router.post("/",
             responses={
                 200: {"model": ContentSchema},
                 422: {"model": ErrorResponse},
                 403: {"model": ErrorResponse}
             },
             dependencies=[Depends(JWTBearer())])
async def add_content(request: Request, content: NewContentSchema = Body(...)):
    if allow_user(request):
        content = jsonable_encoder(content)
        new_content = create_content(content)
        if not new_content:
            raise HTTPException(422, "We could not create the new content")
        return new_content


@router.put("/{content_id}",
            responses={
                200: {"model": ContentSchema},
                422: {"model": ErrorResponse},
                403: {"model": ErrorResponse}
            },
            dependencies=[Depends(JWTBearer())])
async def update(request: Request, content_id: str, data: NewContentSchema = Body(...)):
    if allow_user(request):
        content = jsonable_encoder(data)
        if 'id' in content:
            del content['id']
        updated = update_content(content_id, content)
        if not updated:
            raise HTTPException(422, "We could not update the content")
        return updated


@router.delete("/{content_id}", dependencies=[Depends(JWTBearer())])
async def delete(request: Request, content_id: str):
    if allow_user(request):
        removed = delete_content(content_id)
        if removed:
            return {"result": True}
        raise HTTPException(422, "The method was not deleted")


# Check if the user is admin
def allow_user(request) -> bool:
    user_role = ""
    if 'authorization' in request.headers:
        try:
            user_role = get_role_from_token(request.headers['authorization'].split(" ")[1])
        except IndexError:
            user_role = ""
    if user_role != 'admin':
        raise HTTPException(403, "You are not allowed to make this action")
    return True
