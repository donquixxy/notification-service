from typing import Any, TypeVar, Generic

from pydantic import BaseModel

T = TypeVar('T')

class APIBaseResponse(BaseModel, Generic[T]):
    message:str
    data:T


def success_response(msg:str, data:Any) -> APIBaseResponse:
    return APIBaseResponse(message=msg, data=data)

