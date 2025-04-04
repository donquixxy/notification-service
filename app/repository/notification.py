import json
from importlib.resources import contents

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from abc import ABC, abstractmethod
import uuid

from app.dao.notification import NotificationCreate, NotificationUpdate
from app.models.notification import Notification
from datetime import datetime, timezone, timedelta


class NotificationRepositoryInterface(ABC):
    @abstractmethod
    def create(self, payload:NotificationCreate) -> Notification|None:
        pass

    @abstractmethod
    def update(self, payload:NotificationUpdate) -> Notification|None:
        pass


class NotificationRepository(NotificationRepositoryInterface):
    def __init__(self, db:Session):
        self.db:Session = db

    def create(self, payload:NotificationCreate) -> Notification | None:
        now = datetime.now(timezone(timedelta(hours=8)))
        new_notif = Notification(
            id=str(uuid.uuid4()),
            user_id=payload.user_id,
            created_at=now,
            content=payload.content,
            updated_at=now,
        )
        try:
            self.db.add(new_notif)
            self.db.commit()
            self.db.refresh(new_notif)

            return new_notif
        except SQLAlchemyError as e:
            print(f'[NotificationRepository] - failed to create notification: {e}')
            self.db.rollback()
            return None

    def update(self, payload:NotificationUpdate) -> Notification | None:
        now = datetime.now(timezone(timedelta(hours=8)))
        result:Notification | None = self.db.get(entity=Notification,ident=payload.id)

        if not result:
            raise Exception("Notification data with id not found")

        try:
            if payload.content is not None:
                result.content = payload.content

            if payload.user_id is not None:
                result.user_id = payload.user_id

            result.updated_at = now

            self.db.commit()
            self.db.refresh(result)
            return result
        except SQLAlchemyError as e:
            self.db.rollback()
            raise Exception(f'Failed to update notification with error {e}')