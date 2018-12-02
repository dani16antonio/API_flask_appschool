from db import db

class UserModel(db.Model):
    __tablename__='user'
    id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    username=db.Column(db.String(20))
    password=db.Column(db.String(20))
    email=db.Column(db.String(20))
    def __init__(self,username,password,email):
        self.id=0
        self.username=username
        self.password=password
        self.email=email
    def insert_into_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls,name):
        return cls.query.filter_by(username=name).first()

    @classmethod
    def find_by_id(cls,_id):
        return cls.query.filter_by(id=_id).first()
