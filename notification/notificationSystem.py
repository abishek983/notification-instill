from .notification import NotificationFactoryImpl
from .notifcationSender import NotificationSender

class NotificationSystem:
    def __init__(self):
        self.users = []
        self.notifications = []

    def add_user(self, user):
        self.users.append(user)

    def send_notification(self, db, notification):
        self.notifications.append(notification)
        for user in self.users:
            notification_system = NotificationSender(user)
            notification_system.update(db, notification)

# Usage
# user1 = NotificationSender("Alice")
# user2 = NotificationSender("Bob")

# notification_system = NotificationSystem()
# notification_system.add_user(user1)
# notification_system.add_user(user2)

# notification_factory = NotificationFactoryImpl()

# normal_notification = notification_factory.create_notification("New Update", "Check out the latest news!")
# urgent_notification = notification_factory.create_notification("Urgent Alert", "Action required immediately!", "urgent")

# notification_system.send_notification(normal_notification)
# notification_system.send_notification(urgent_notification)
