from webob import Request
from typing import Optional
from utils.decorators import jsonresponse, api

USERS = [
    {"id": 1, "name": "Jim"},
    {"id": 2, "name": "Bruce"},
    {"id": 3, "name": "Dick"},
]


@api
@jsonresponse
def get_users(
        id: Optional[str] = None,
        name: Optional[str] = None
) -> dict:
    filter_by_name = lambda user, name: user if user.get("name", "") == name else None
    filter_by_id = lambda user, id: user if user.get("id", "") == id else None
    data = None
    for user in USERS:
        if id:
            data = filter_by_id(user, id)
        elif name:
            data = filter_by_name(user, name)
        if data:
            return data
    return {"users": USERS}
