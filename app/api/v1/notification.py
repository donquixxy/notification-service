from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

from app.core.database import get_db_instance
from app.dao.notification import NotificationCreate, NotificationSchema
from app.payload.response import APIBaseResponse, success_response
from app.repository.notification import NotificationRepository
from app.services.notification import NotificationService

router = APIRouter(prefix='/notification', tags=['notification'])
@router.post("", response_model=APIBaseResponse[NotificationSchema])
def create(payload: NotificationCreate, db: Session = Depends(get_db_instance)):
    repository = NotificationRepository(db)
    service = NotificationService(repository)
    result = service.create(payload)

    if not result:
        raise HTTPException(status_code=40, detail="Failed to create notification")

    return success_response(msg="successfully created notification", data=NotificationSchema.model_validate(result))
