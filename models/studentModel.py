import sqlite3
from db import db
class StudentModel(db.Model):
    __tablename__='student'
    id=db.Column(db.Integer,autoincrement=True,primary_key=True)
    name=db.Column(db.String(15))
    lastname=db.Column(db.String(15))
    age=db.Column(db.Integer)

    def __init__(self,name, lastname,age):
        self.name=name
        self.lastname=lastname
        self.age=age

    def insert_into_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls,name):
        return cls.query.filter_by(name=name).first()

    def json(self):
        return{
        'id':self.id,
        'name':self.name,
        'lastname':self.lastname,
        'age':self.age
        }
