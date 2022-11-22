from app import ma


class CountrySchema(ma.Schema):
    class Meta:
        # Fields to expose
        fields = ("id", "name", "name_global", "code", "status", "code_alpha2", "code_alpha3")
        ordered = True
