from flask import Flask
import os
from flask.ext.sqlalchemy import SQLAlchemy
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "hard"
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'datanihao.sqlite')
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
db = SQLAlchemy(app)
db.create_all()  # 创建表
# 蓝图注册
from app.blog import blog as blog_blueprint
from app.admin import admin as admin_blueprint
app.register_blueprint(blog_blueprint)
app.register_blueprint(admin_blueprint)
# 配置数据库


# import os
# import pymysql
# basedir = os.path.abspath(os.path.dirname(__file__))
# DEBUG = True
# pymysql.install_as_MySQLdb()
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_nihao.sqlite')
# # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/flaskdm?utf8'
# SECRET_KEY = 'hard'
# SQLALCHEMY_COMMIT_ON_TEARDOWN = False