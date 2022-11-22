from app import ma


class GroupSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name")
        ordered = True
