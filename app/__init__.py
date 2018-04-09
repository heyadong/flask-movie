from flask import Flask,render_template
import os
import pymysql
from flask_sqlalchemy import SQLAlchemy
app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
app.config['SECRET_KEY'] = "hardguess"
# URI的格式链接mysql: 驱动+链接数据库+：//用户名：密码@数据库地址
# mysql 链接方式："pymysql+mysql://root：password@localhost:3306/flaskdev
# app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(basedir, 'datanihao.sqlite')
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:password@localhost:3306/my_db?charset=utf8'# 配置数据库
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['UP_DIR'] =os.path.join(os.path.abspath(os.path.dirname(__file__)),"static/uploads/")
db = SQLAlchemy(app)
# db.create_all()  # 创建表
# 蓝图注册
from app.blog import blog as blog_blueprint
from app.admin import admin as admin_blueprint
app.register_blueprint(blog_blueprint)
app.register_blueprint(admin_blueprint,url_prefix="/admin")


@app.errorhandler(404)
def page_not_found(error):
    return render_template('home/404.html')


# import os
# import pymysql
# basedir = os.path.abspath(os.path.dirname(__file__))
# DEBUG = True
# pymysql.install_as_MySQLdb()
# SQLALCHEMY_DATABASE_URI = 'sqlite:///' + os.path.join(basedir, 'data_nihao.sqlite')
# # SQLALCHEMY_DATABASE_URI = 'mysql://root:password@localhost:3306/flaskdm?utf8'
# SECRET_KEY = 'hard'
# SQLALCHEMY_COMMIT_ON_TEARDOWN = False