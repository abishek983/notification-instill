import sys
sys.path.append("..")
from models import Notification
from sqlalchemy.orm import Session

class Observer:
    def update(self, notification):
        pass

class NotificationSender(Observer):
    def __init__(self, username):
        self.username = username

    def update(self, db:Session, notification):
        """logic to persist data in DB"""
        notification = Notification(user=self.username, title=notification.title, description=notification.description, identifier=notification.identifier)
        db.add(notification)
        db.commit()
        db.refresh(notification)
        print(f"User {self.username} received notification: {notification}")