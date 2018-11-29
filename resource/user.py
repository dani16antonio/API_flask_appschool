from flask_restful import Resource, reqparse
from models.userModel import UserModel
class UserRegister(Resource):
    parser=reqparse.RequestParser()
    parser.add_argument('username',
                        type=str,
                        required=True,
                        help="can't be blank")

    parser.add_argument('password',
                        type=str,
                        required=True,
                        help="can't be blank")

    parser.add_argument('email',
                        type=str,
                        required=True,
                        help="can't be blank")
    def post(self):
        data=UserRegister.parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {'message':'User already exists.'},400
        user=UserModel(data['username'],data['password'],data['email'])
        user.insert_into_database()
        return{'message':'user create Succesfully.'},201
