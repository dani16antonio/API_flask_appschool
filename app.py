#importamos la librería para construir la API
from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager
#pip install flask_jwt_extended
from resource.student import Student
from resource.user import UserRegister,UserLogin

#from models.student import studentModel
#importamos nuestros recursos

app=Flask(__name__)
app.config['SQLACHEMY_DATABASE_URI']='sqlite///data.db'
app.config['SQLACHEMY_TRACK_MODIFICATIONS']=False
app.config['PROPAGATE_EXCEPTIONS']=True
app.secret_key='esternocleidomastoideo'
api=Api(app)

@app.before_first_request
def create_tables():
    db.create_all()
    
jwt=JWTManager(app)


api.add_resource(UserRegister,'/register')
api.add_resource(Student,'/student')
api.add_resource(UserLogin,'/login')
if __name__=='__main__':
    from db import db
    db.init_app(app)
    app.run()
