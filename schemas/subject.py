from ma import ma
from models.subjectModel import SubjectModel

class SubjectSchema(ma.ModelSchema):
    class Meta:
        model=SubjectModel
        dump_only=("id",)
