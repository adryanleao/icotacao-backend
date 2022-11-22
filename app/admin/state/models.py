from app import db
from app.services.sqlalchemy.models import BaseModel
from app.admin.country.models import Country


class State(db.Model, BaseModel):
    __tablename__ = 'state'

    name = db.Column(db.String(256))
    uf = db.Column(db.String(2), nullable=False)
    status = db.Column(db.Integer, default=1)

    country_id = db.Column(db.Integer, db.ForeignKey('country.id'))

    def _get_country(self):
        return db.session.using_bind('slave').query(Country).filter(Country.id == self.country_id,
                                                                    Country.deleted_at == None).first()

    country = property(_get_country)

    def create_item(self, json):
        self.country_id = json['country']['id']
        self.name = json['name']
        self.uf = json['uf']
        return self

    def update_item(self, json):
        self.country_id = json['country']['id']
        self.name = json.get('name', self.name)
        self.uf = json.get('uf', self.uf)
        self.status = json.get('status', self.status)
        return self
