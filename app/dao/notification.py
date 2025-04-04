from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel
from typing import Any, Optional

class NotificationSchema(BaseModel):
    id: str
    user_id: str
    content: Any
    created_at: datetime
    updated_at: datetime

    model_config = {
        "from_attributes" : True,
        "to_attributes" : True,
    }


@dataclass
class NotificationCreate(BaseModel):
    user_id:str
    content:dict[str, Any]

@dataclass
class NotificationUpdate(BaseModel):
    id:str
    user_id:Optional[str] = None
    content:Optional[dict[str, Any]] = None

@dataclass
class NotificationFilter(BaseModel):
    id:Optional[str] = None
    user_id:Optional[str] = None