from marshmallow import Schema, fields
from models.userModel import  UserModel
from ma import ma
from models.studentModel import StudentModel
class StudentSchema(ma.ModelSchema):
    class Meta:
        model=StudentModel
        dump_only=("id",)