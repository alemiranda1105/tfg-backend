from pydantic import ValidationError

from server.models.Changelog import BaseChangelogSchema, ChangelogSchema


def changelog_helper(content_data) -> dict:
    return {
        "id": str(content_data['_id']),
        "description": content_data['description'],
        "date": content_data['date']
    }


def validation_changelog_helper(content, is_new: bool):
    try:
        if is_new:
            BaseChangelogSchema(
                description=content['description'],
                date=content['date']
            )
        else:
            ChangelogSchema(
                id=str(content['_id']),
                description=content['description'],
                date=content['date']
            )
    except ValidationError:
        return False
    return True
