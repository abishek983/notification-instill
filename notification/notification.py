class NotificationFactory:
    def create_notification(self, title, description, identifier=None):
        pass

class Notification:
    def __init__(self, title, description, identifier=None):
        self.title = title
        self.description = description
        self.identifier = identifier

class TextNotification(Notification):
    pass

class WhatsAppNotification(Notification):
    pass

class EventNotification(Notification):
    pass

class NotificationFactoryImpl(NotificationFactory):
    def create_notification(self,  title, description, identifier=None):
        if identifier == "text" or "none":
            return TextNotification(title, description, identifier)
        elif identifier == "whatsApp":
            return WhatsAppNotification(title, description, identifier)
        elif identifier == "event":
            return EventNotification(title, description, identifier)
        else:
            raise ValueError("Invalid notification type")

# Usage
notification_factory = NotificationFactoryImpl()
# normal_notification = notification_factory.create_notification("New Update", "Check out the latest news!")
# urgent_notification = notification_factory.create_notification("Urgent Alert", "Action required immediately!", "urgent")
# event_notification = notification_factory.create_notification("Upcoming Event", "Join us for an exciting event!", "event")
