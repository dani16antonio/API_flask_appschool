from marshmallow import Schema,fields

class StudentSchema(Schema):
    name=fields.Str(required=True)
    lastname=fields.Str(required=True)
    gender=fields.Str(required=True)
    id=fields.Int()
    doc=fields.Str(required=True)