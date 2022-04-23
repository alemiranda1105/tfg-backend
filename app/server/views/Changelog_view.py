from typing import List

from fastapi import APIRouter, HTTPException, Body, Request, Depends
from fastapi.encoders import jsonable_encoder

from app.server.auth.auth_bearer import JWTBearer
from app.server.auth.auth_handler import get_role_from_token
from app.server.controllers.Changelog_controller import get_all_changelog, get_changelog_by_id, create_changelog, \
    update_changelog, delete_changelog
from app.server.models.Changelog import ChangelogSchema, BaseChangelogSchema
from app.server.models.CustomResponse import ErrorResponse

router = APIRouter(
    prefix="/changelog",
    tags=["changelog"]
)


@router.get("/",
            responses={
                200: {"model": List[ChangelogSchema]},
                404: {"model": ErrorResponse}
            })
async def show_all_changelog():
    content = get_all_changelog()
    if len(content) <= 0:
        raise HTTPException(404, "We could not find any content")
    return content


@router.get("/{changelog_id}",
            responses={
                200: {"model": ChangelogSchema},
                404: {"model": ErrorResponse}
            })
async def show_content_by_id(changelog_id: str):
    content = get_changelog_by_id(changelog_id)
    if not content:
        raise HTTPException(404, "We could not find any content")
    return content


@router.post("/",
             responses={
                 200: {"model": ChangelogSchema},
                 422: {"model": ErrorResponse},
                 403: {"model": ErrorResponse}
             },
             dependencies=[Depends(JWTBearer())])
async def add_content(request: Request, content: BaseChangelogSchema = Body(...)):
    if allow_user(request):
        content = jsonable_encoder(content)
        new_content = create_changelog(content)
        if not new_content:
            raise HTTPException(422, "We could not create the new content")
        return new_content


@router.put("/{changelog_id}",
            responses={
                200: {"model": ChangelogSchema},
                422: {"model": ErrorResponse},
                403: {"model": ErrorResponse}
            },
            dependencies=[Depends(JWTBearer())])
async def update(request: Request, changelog_id: str, data: BaseChangelogSchema = Body(...)):
    if allow_user(request):
        content = jsonable_encoder(data)
        if 'id' in content:
            del content['id']
        updated = update_changelog(changelog_id, content)
        if not updated:
            raise HTTPException(422, "We could not update the content")
        return updated


@router.delete("/{changelog_id}", dependencies=[Depends(JWTBearer())])
async def delete(request: Request, changelog_id: str):
    if allow_user(request):
        removed = delete_changelog(changelog_id)
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