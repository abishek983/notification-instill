from typing import List, Union
from datetime import datetime
from pydantic import BaseModel


class NotificationBase(BaseModel):
    title: str
    description: Union[str, None] = None


class Notificationcreate(NotificationBase):
    pass


class Notification(NotificationBase):
    id: int
    identifier: str
    created_at: datetime

    class Config:
        orm_mode = True
