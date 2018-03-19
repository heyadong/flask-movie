# coding:utf-8
from flask import render_template,url_for,request,redirect
from . import blog
from app.models import Admin
from app import db

@blog.route("/",methods=["GET","POST"])
def index():

    # 增加admin账号
    # from werkzeug.security import generate_password_hash
    # admin = Admin(name='heyadong', password=generate_password_hash('502505'), is_super=0, role_id=1)
    # db.session.add(admin)
    # db.session.commit()
    # print('')
    # 查询
    # user = Admin.query.filter_by(role_id=1).first()
    # print(request.args.get('name'))
    return render_template('index.html')

@blog.route('/login/')
# 注意路由使用'/login/'
def login():
    return render_template('home/login.html')

@blog.route('/logout/')
def logout():
    # redirect()重定向到登陆页面
    return redirect(url_for("blog.login"))

