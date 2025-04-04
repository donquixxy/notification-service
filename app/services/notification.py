from abc import ABC, abstractmethod
from app.models.notification import Notification
from app.dao.notification import NotificationCreate
from app.repository.notification import NotificationRepositoryInterface


class NotificationServiceInterface(ABC):
    @abstractmethod
    def create(self, payload:NotificationCreate) -> Notification|None:
        pass


class NotificationService(NotificationServiceInterface):

    def __init__(self, repository:NotificationRepositoryInterface):
        self.repository = repository

    def create(self, payload:NotificationCreate) -> Notification|None:
        try:
            return self.repository.create(payload)
        except Exception as e:
            print(f'[NotificationService] - Failed to create notification: {e}')
            return None
