from sqlalchemy import func

from app.admin.notification.models import Notification, NotificationSend
from app.client.quote.models import Quote


def count_notifications_and_quotes(user_id):
    notifications = NotificationSend.query.with_entities(Notification.quote_id,
                                                         NotificationSend.id,
                                                         Quote.status)\
        .join(Notification, NotificationSend.notification_id == Notification.id) \
        .join(Quote, Quote.id == Notification.quote_id) \
        .filter(NotificationSend.user_id == user_id).all()
    quotes = Quote.query.with_entities(func.count(Quote.id).label("total")) \
        .filter(Quote.user_id == user_id, Quote.status == 0).first()

    return {
        "notification_count": len(notifications),
        "quote_count": quotes.total
    }
