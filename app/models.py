from app import db
from datetime import datetime
from collections import OrderedDict

   
class Staff(db.Model):
    __tablename__ = "stafftbl"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    isAdmin = db.Column(db.Boolean, default=False)
    accessToken = db.Column(db.String(200), nullable=False)
    refreshToken = db.Column(db.String(200),nullable=False)
    password = db.Column(db.String(255),nullable=False)
    createdAt = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "email": self.email,
            "isAdmin": self.isAdmin,
            "createdAt": self.createdAt
        }


class Student(db.Model):
    __tablename__ = "studenttbl"
    id = db.Column(db.Integer, primary_key=True)
    roll_no = db.Column(db.String(30), nullable=False)
    firstname = db.Column(db.String(20), nullable=False)
    middlename = db.Column(db.String(20), nullable=False)
    lastname = db.Column(db.String(20), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    mobileno = db.Column(db.String(11), nullable=False)
    course = db.Column(db.String(20), nullable = False)
    year = db.Column(db.String(10), nullable = False)


    def to_dict(self):
        return OrderedDict({
        "id": self.id, 
        "roll_no": self.roll_no,
        "firstname": self.firstname,
        "middlename": self.middlename,
        "lastname": self.lastname,
        "age": self.age,
        "email": self.email,
        "mobileno": self.mobileno,
        "course": self.course,
        "year": self.year
    })

    
