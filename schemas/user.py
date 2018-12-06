from ma import ma
from models.userModel import UserModel

class UserSchema(ma.ModelSchema):
    class Meta:
        model=UserModel
        load_only=("password","id")#a list or tuple of fields to skip during serialization, we don't send this value
        dump_only=("id",)#a list or tuple of fields to skip during deserialization, read-only fields, we don't receive this value, we generate it automatically