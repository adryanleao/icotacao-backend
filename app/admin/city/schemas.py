from marshmallow import Schema, fields

from app.admin.state.schemas import StateSchema


class CitySchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "status")
        ordered = True

    state = fields.Nested(StateSchema())