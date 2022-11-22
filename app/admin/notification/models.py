from app import db
from app.services.sqlalchemy.models import BaseModel


class Notification(db.Model, BaseModel):
    __tablename__ = 'notification'

    icon = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    status = db.Column(db.Boolean(), nullable=False, default=True)

    quote_id = db.Column(db.Integer, db.ForeignKey('quote.id'))

    def create_item(self, json):
        self.quote_id = json.get('quote_id', None)
        self.icon = json['icon']
        self.name = json['name']
        self.description = json['description']
        return self

    def update_item(self, json):
        self.icon = json.get('icon', self.icon)
        self.name = json.get('name', self.name)
        self.description = json.get('description', self.description)
        self.status = json.get('status', self.status)
        return self


class NotificationSend(db.Model, BaseModel):
    __tablename__ = 'notification_send'

    icon = db.Column(db.String(255), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(255), nullable=False)
    view_date = db.Column(db.DateTime)

    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    notification_id = db.Column(db.Integer, db.ForeignKey('notification.id'))

    def create_item(self, json):
        self.icon = json['icon']
        self.name = json['name']
        self.description = json['description']
        self.user_id = json['user_id']
        self.notification_id = json['notification_id']
        return self

    def update_item(self, json):
        self.view_date = json.get('view_date', self.view_date)
        return self
