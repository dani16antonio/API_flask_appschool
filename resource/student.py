from flask_restful import Resource
from flask_jwt import jwt_required
from models.studentModel import StudentModel
from marshmallow import ValidationError
from flask import request
from schemas.student import StudentSchema

student_schema=StudentSchema()
class Student(Resource):

    #@jwt_required
    def get(self):
        try:
            data=student_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages,401
        student=StudentModel.find_by_document(data['doc'])
        return student_schema.dump(student)

    #@jwt_required
    def post(self):
        try:
            data=student_schema.load(request.get_json())
        except ValidationError as err:
            return err.messages,401
        if StudentModel.find_by_document(data['doc']):
            return{'message':'Student already exists.'},400
        #student=StudentModel(data['doc'], data['name'], data['lastname'], data['gender'], data['birthday'])
        student = StudentModel(**data)
        try:
            student.insert_into_database()
        except:
            return{'message':'Internal server error.'},500
        return student_schema.dump(student),201
