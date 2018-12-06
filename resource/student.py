from flask_restful import Resource
from flask_jwt_extended import jwt_required, get_jwt_claims, fresh_jwt_required
from models.studentModel import StudentModel
from marshmallow import ValidationError
from flask import request
from schemas.student import StudentSchema

student_schema=StudentSchema()
#set resoruce schema

STUDENT_NOT_FOUND="Oh!, looks like any student have {} document, please, try again."
STUDENT_ALREADY_EXISTS="Oh!, looks like a student alaready have {} doc, please, try again."
DONT_HAVE_PERMISSION="You do not have permission to make that query."
STUDENT_DELETED=""
class Student(Resource):

    @jwt_required
    def get(self,doc):
        claims=get_jwt_claims()
        if not claims['view']:
            return {'msg':DONT_HAVE_PERMISSION}

        student=StudentModel.find_by_document(doc)
        if student:
            return student_schema.dump(student),200
        return {"msg":STUDENT_NOT_FOUND.format(doc)},404

    @jwt_required
    def post(self,doc):
        claims=get_jwt_claims()
        if not claims['write']:
            return {'msg':DONT_HAVE_PERMISSION}

        if StudentModel.find_by_document(doc):
            return {"msg":STUDENT_ALREADY_EXISTS.format(doc)},400
        student_data = request.get_json()
        student_data['doc']=doc
        student=student_schema.load(student_data)
        student.insert_into_database()
        return student_schema.dump(student),201

    @jwt_required
    def put(self,doc):
        claims=get_jwt_claims()
        if not claims['update']:
            return {'msg':DONT_HAVE_PERMISSION}

        student_data=request.get_json()
        student_data['doc'] = doc
        #get data from the request and set doc that came by param
        student=StudentModel.find_by_document(doc)
        #find student by doc and get a StudentModel object
        if student:
            student.doc=student_data['doc']
            student.name=student_data['name']
            student.lastname = student_data['lastname']
            student.gender = student_data['gender']
            #if student exists, we'll update his info
        else:
            student=student_schema.load(student_data)
            #if student don't exists, we'll create that student
        student.insert_into_database()
        return student_schema.dump(student), 200
        # save student object into database and return student data

    @jwt_required
    @fresh_jwt_required
    def delete(self, doc):
        claims = get_jwt_claims()
        if not claims['delete']:
            return {'msg': DONT_HAVE_PERMISSION}, 401
        student = StudentModel.find_by_document(doc)
        if student:
            student.delete_from_database()
            return {'msg': STUDENT_DELETED}, 200
        return {'msg': STUDENT_NOT_FOUND}, 404
