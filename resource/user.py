from flask_jwt_extended import create_access_token, create_refresh_token
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask import request
from marshmallow import ValidationError
from models.userModel import UserModel
from schemas.user import UserSchema
user_schema=UserSchema()
class UserRegister(Resource):
    def post(self):
        try:
            request_json = request.get_json()
            data=user_schema.load(request_json)
        except ValidationError as err:
            return err.messages,401
        if UserModel.find_by_username(data['username']):
            return {'message':'User already exists.'},400
        user=UserModel(data['username'],data['password'],data['email'])
        user.insert_into_database()
        return{'message':'user created Succesfully.'},201

class UserLogin(Resource):

    @classmethod
    def post(cls):
        try:
            request_json = request.get_json()
            data=user_schema.load(request_json)
        except ValidationError as err:
            return err.messages,401
        user=UserModel.find_by_username(data['username'])
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.email,fresh=True)
            refresh_token=create_refresh_token(user.email)
            #access_toker and refresh_token created using user's email
            return {
                'access_token':access_token,
                'refresh_token':refresh_token
            }
        return {
            'message':"Wow!, look like that user don't exist."
        }
