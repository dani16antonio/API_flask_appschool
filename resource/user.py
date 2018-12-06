from flask_jwt_extended import (
    create_access_token,
    create_refresh_token,
    jwt_refresh_token_required, get_jwt_identity, get_jwt_claims, jwt_required)
from flask_restful import Resource
from werkzeug.security import safe_str_cmp
from flask import request
from marshmallow import ValidationError
from models.userModel import UserModel
from schemas.user import UserSchema

user_schema = UserSchema()

USER_ALREADY_EXISTS = "User already exists."
USER_CREATED = "user created Succesfully."
USER_DONT_EXISTS = "Wow!, look like that user don't exist."
DONT_HAVE_PERMISSION="You do not have permission to make this query."

class UserRegister(Resource):
    def post(self):
        request_json = request.get_json()
        user = user_schema.load(request_json)
        if UserModel.find_by_username(user.username):
            return {'msg': USER_ALREADY_EXISTS}, 400
        user.insert_into_database()
        return {'msg': USER_CREATED}, 201

class UserLogin(Resource):
    def post(self):
        request_json = request.get_json()
        data = user_schema.load(request_json)
        user = UserModel.find_by_username(data.username)
        if user and safe_str_cmp(user.password, data.password):
            access_token = create_access_token(identity=user.userType, fresh=True)
            refresh_token = create_refresh_token(user.email)
            # access_toker and refresh_token created using user's email
            return {
                'access_token': access_token,
                'refresh_token': refresh_token
            }
        return {
            'msg': USER_DONT_EXISTS
        }

class UpdateData(Resource):

    @jwt_required
    def get(self,username):
        user=UserModel.find_by_username(username)
        if user:
            return user_schema.dump(user),200
        return {'msg':USER_DONT_EXISTS}, 404


    @jwt_refresh_token_required
    def put(self,username):
        claims=get_jwt_claims()
        if not claims['update']:
            return {'msg':DONT_HAVE_PERMISSION},401

        user_json=request.get_json()
        user_json['username']=username
        data=user_schema.load(user_json)
        user=UserModel.find_by_username(username)
        if user:
            user.username=data['username']
            user.password=data['password']
            user.email=data['email']
        else:
            user=user_schema.load(user_json)
        user.insert_into_database()
        return user_schema.dump(user_json), 200

class TokenRefreseh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user=get_jwt_identity()
        new_token=create_access_token(identity=current_user, fresh=False)
        return {'access_token': new_token}, 200
