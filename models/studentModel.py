import sqlite3
from db import db
from datetime import date
from dateutil.relativedelta import relativedelta
#pip install python-dateutil

class StudentModel(db.Model):
    __tablename__='student'

    #todo:save a student photo
    id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    doc=db.Column(db.String(15))#00-0000-000000
    gender=db.Column(db.String(15))
    #birthday=db.Column(db.DateTime)
    name=db.Column(db.String(15))
    lastname=db.Column(db.String(15))

    def __init__(self,doc,name, lastname,gender):
        self.id=0
        self.doc=doc
        self.name=name
        self.lastname=lastname
        self.gender=gender

    def insert_into_database(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_database(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_document(cls,doc):
        return cls.query.filter_by(doc=doc).first()
