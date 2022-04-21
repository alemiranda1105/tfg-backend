from pydantic import ValidationError

from server.models.Content import ContentSchema, NewContentSchema


def content_helper(content_data) -> dict:
    return {
        "id": str(content_data['_id']),
        "title": content_data['title'],
        "text": content_data['text']
    }


def validation_content_helper(content, is_new: bool):
    try:
        if is_new:
            NewContentSchema(
                title=content['title'],
                text=content['text']
            )
        else:
            ContentSchema(
                id=str(content['_id']),
                title=content['title'],
                text=content['text']
            )
    except ValidationError:
        return False
    return True
