from app.admin.notification.models import Notification
from app.client.quote.models import Quote


def get_quote_from_notification(notification_id):
    notification = Notification.query.filter(Notification.id == notification_id).first()
    quote = Quote.query.filter(Quote.id == notification.quote_id).first()
    if quote:
        return quote
