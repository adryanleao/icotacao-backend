from marshmallow import Schema


class SegmentSchema(Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "description", "status")
        ordered = True
