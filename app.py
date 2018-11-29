#importamos la librería para construir la API
from flask import Flask
from flask_restful import Api
from flask_jwt import JWT
from security import authenticate,identity
from resource.student import Student
from resource.user import UserRegister

#from models.student import studentModel
#importamos nuestros recursos

app=Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI']='sqlite///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS']=False
app.secret_key='esternocleidomastoideo'
api=Api(app)
@app.before_first_request
def create_tables():
    db.create_all()
    
jwt=JWT(app,authenticate,identity)


api.add_resource(UserRegister,'/register')
api.add_resource(Student,'/student/<string:name>')
if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run()
