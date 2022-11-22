from app import db
from app.admin.state.models import State
from app.services.sqlalchemy.models import BaseModel


class City(db.Model, BaseModel):
    __tablename__ = 'city'

    name = db.Column(db.String(256))
    status = db.Column(db.Integer, default=1)

    state_id = db.Column(db.Integer, db.ForeignKey('state.id'))

    state = db.relationship(State, uselist=False, backref="city")

    def _get_state(self):
        return db.session.using_bind('slave').query(State).filter(State.id == self.state_id,
                                                                 State.deleted_at == None).first()

    state = property(_get_state)

    def create_item(self, json):
        self.state_id = json['state']['id']
        self.name = json['name']
        return self

    def update_item(self, json):
        self.state_id = json['state']['id']
        self.name = json.get('name', self.name)
        self.status = json.get('status', self.status)
        return self
