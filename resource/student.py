from flask_restful import Resource, reqparse
from flask_jwt import jwt_required
from models.studentModel import StudentModel
class Student(Resource):
    parser=reqparse.RequestParser()

    #set get lastname
    parser.add_argument('lastname',
                        type=str,
                        required=True,
                        help="can't be blank")
    #set get age
    parser.add_argument('age',
                        type=str,
                        required=True,
                        help="can't be blank")

    @jwt_required()
    def get(self,name):
        student=StudentModel.find_by_name(name)
        return student.json()

    @jwt_required()
    def post(self,name):
        if StudentModel.find_by_name(name):
            return{'message':'Student already exists.'},400
        data=Student.parser.parse_args()
        student=StudentModel(name,data['lastname'],data['age'])
        try:
            student.insert_into_database()
        except Exception as e:
            return{'message':'Internal server error.'},500
        return student.json(),201
