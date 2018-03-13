# models
from datetime import datetime
from app import db


class Students(db.Model):
    __tablename__ = "student_info"  ## 表名
    id = db.Column(db.Integer, primary_key=True, autoincrement=True) #
    name = db.Column(db.String(50), nullable=False)
    sex = db.Column(db.String(10))
    id_num = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default=datetime.utcnow())

    def __repr__(self):
        return '<students %r>' % self.name


class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String, nullable=False)
    pw = db.Column(db.String(60),nullable=False)

    def __repr__(self):
        return '<user %r>' % self.username

