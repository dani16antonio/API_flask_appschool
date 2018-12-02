from db import db
class SubjectModel(db.Model):
    __tablename__='subject'
    id=db.Column(db.Integer, autoincrement=True,primary_key=True)
    name=db.Column(db.String(20))

    def __init__(self,name):
        self.name=name

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
        'name':self.name
        }
