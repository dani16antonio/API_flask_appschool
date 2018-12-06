#importamos la librería para construir la API
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
#pip install flask_jwt_extended
from werkzeug.security import safe_str_cmp

from flask import jsonify
from ma import ma
from marshmallow import ValidationError
from resource.student import Student
from resource.user import UserRegister,UserLogin,UpdateData, TokenRefreseh

#from models.student import studentModel
#importamos nuestros recursos

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key='esternocleidomastoideo'
api = Api(app)

YOU_DONT_HAVE_USERTYPE="your user had a problem with its status, please contact system admin"

@app.before_first_request
def create_tables():
    db.create_all()

@app.errorhandler(ValidationError)
def handler_marshmallow_validation(err):
    return jsonify(err.messages),400

jwt=JWTManager(app)

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    claims = {}
    if not identity:
        return {'msg':YOU_DONT_HAVE_USERTYPE}
    if safe_str_cmp(identity,"Estudiante"):
        claims['view'] = True
        claims['write'] = False
        claims['delete'] = False
        claims['update'] = False
    elif safe_str_cmp(identity,'Administrativo'):
        claims['view'] = True
        claims['write'] = True
        claims['delete'] = False
        claims['update'] = True
    elif safe_str_cmp(identity,"SuperSu"):
        claims['view'] = True
        claims['write'] = True
        claims['delete'] = True
        claims['update'] = True
    else:
        claims['view'] = False
        claims['write'] = False
        claims['delete'] = False
        claims['update'] = False
    return claims

api.add_resource(UserRegister,'/register')
api.add_resource(TokenRefreseh,'/refresh')

api.add_resource(UpdateData,'/settings/<string:username>')
api.add_resource(Student,'/student/<string:doc>')
api.add_resource(UserLogin,'/login')
if __name__=='__main__':
    from db import db
    db.init_app(app)
    ma.init_app(app)
    app.run()#debug=True)
