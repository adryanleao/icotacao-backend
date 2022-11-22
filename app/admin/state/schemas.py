from app import ma


class StateSchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "uf", "status")
        ordered = True
