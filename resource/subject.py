from flask_restful import Resource
from flask_jwt import jwt_required
from models.subjectModel import SubjectModel

class Subject(Resource):

    @jwt_required
    def get(self,name):
        subject=SubjectModel.find_by_name(name)
        return subject.json()

    @jwt_required
    def post(self,name):
        if SubjectModel.find_by_name(name):
            return{'message':'Student already exists.'},400
        # TODO: get info from the header of url?
