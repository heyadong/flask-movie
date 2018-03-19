# coding=utf-8
__author__ = "heyadong"

from datetime import datetime
from app import db
# flask models.py 用于定义数据表。在app.__init__.py 中定义好db = SQLAlchemy(app) 导入db
# 常用的方法:
# db.Column(db.String(500)定义数据列


class User(db.Model):
    __tablename__ = 'user'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # 用户名
    password = db.Column(db.String(100))
    phone = db.Column(db.String(11))
    info = db.Column(db.Text)  # 简介
    pagra = db.Column(db.String(255), unique=True)  # 头像
    add_time = db.Column(db.DateTime, default=datetime.utcnow())
    uuid = db.Column(db.String(255), unique=True)
    userlog = db.relationship('Userlog', backref='user')  # 外键关联
    moviecols = db.relationship('Moviecol', backref='user')
    comments = db.relationship('Comment', backref='user')

    def __repr__(self):
        return '<user %r>' % self.username


# 用户登陆日志表
class Userlog(db.Model):
    __tablename__ = "userlog"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    ip = db.Column(db.String(100))  #
    add_time = db.Column(db.DateTime,  default=datetime.now())

    def __repr__(self):
        return "<Userlog %r>" % self.id


# 标签数据模型
class Tag(db.Model):
    __tablename__ = "tag"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    add_time = db.Column(db.DateTime, default=datetime.now())
    movies = db.relationship('Movie', backref="tag")

    def __repr__(self):
        return "<Tag %r>" % self.name


# 电影表
class Movie(db.Model):
    __tablename = "movie"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    url = db.Column(db.String(255), unique=True)
    info = db.Column(db.Text)
    logo = db.Column(db.String(255), unique=True)
    star = db.Column(db.SmallInteger)
    palynum = db.Column(db.BigInteger)
    commentnum = db.Column(db.BigInteger)  # 评论
    tag_id = db.Column(db.Integer, db.ForeignKey('tag.id'))
    area = db.Column(db.String(255))
    relase_time = db.Column(db.Date)  # 上映时间
    lenth = db.Column(db.String(255))  # 播放时间
    add_time = db.Column(db.DateTime,  default=datetime.now())
    comments = db.relationship("Comment", backref="movie")

    def __repr__(self):
        return "<Movie %r>" % self.title


class Preview(db.Model):
    __tablename__ = 'preview'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    logo = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime,  default=datetime.now())

    def __repr__(self):
        return "<Preview %r>" % self.title


# 评论表
class Comment(db.Model):
    __tablename__ = "comment"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    add_time = db.Column(db.DateTime,  default=datetime.now())


# 电影收藏
class Moviecol(db.Model):
    __tablename__ = "moviecol"
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    movie_id = db.Column(db.Integer, db.ForeignKey('movie.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    add_time = db.Column(db.DateTime,  default=datetime.now())


# 权限表
class Auth(db.Model):
    __tablename__ = 'auth'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    url = db.Column(db.String(255), unique=True)
    add_time = db.Column(db.DateTime,  default=datetime.now())

    def __repr__(self):
        return "<Auth %r>" % self.name


# 角色表
class Role(db.Model):
    __tablename__ = 'role'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    auths = db.Column(db.String(600), )
    add_time = db.Column(db.DateTime,  default=datetime.now())

    def __repr__(self):
        return "<Role %r>" % self.name


# 管理员登陆日志：
class Admin(db.Model):
    __tablename__ = 'admin'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    name = db.Column(db.String(100), unique=True)  # 用户名
    password = db.Column(db.String(100))
    is_super = db.Column(db.SmallInteger)
    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))
    adminlogs = db.relationship('Adminlog', backref='admin')
    oplogs = db.relationship('Oplog', backref='admin')

    def __repr__(self):
        return '<admin %r>' % self.name


# 操作日志
class Adminlog(db.Model):
    __tablename__ = 'adminlog'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 用户名
    ip = db.Column(db.String(100))
    add_time = db.Column(db.DateTime,  default=datetime.now())

    def __repr__(self):
        return "<admin %r>" % self.id


class Oplog(db.Model):
    __tablename__ = 'oplog'
    __table_args__ = {"useexisting": True}
    id = db.Column(db.Integer, primary_key=True)  # id
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.id'))  # 用户名
    ip = db.Column(db.String(100))
    reason = db.Column(db.String(600))
    add_time = db.Column(db.DateTime,  default=datetime.now())

    def __repr__(self):
        return "<Oplog %r>" % self.id



