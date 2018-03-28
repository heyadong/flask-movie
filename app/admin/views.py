from flask import render_template, url_for, redirect,flash ,request,session
from . import admin
from .forms import LoginForm,TagForm
from app.models import Admin,Tag
from app import db
from werkzeug.security import generate_password_hash
from functools import wraps

# 登陆限制。使用装饰器进行登陆限制
def admin_login_req(func):
    @wraps(func)
    def decrated_fuc(*args,**kwargs):
        if session.get("admin") is None:
            return redirect(url_for("admin.login"))
        return func(*args,**kwargs)
    return decrated_fuc


# session.permanent = True  session 过期时间设置，没有设置过期时间默认浏览器关闭session过期


@admin.route('/', methods=["GET", "POST"])
@admin_login_req
def index():
    return render_template("hdmin/index.html")


@admin.route('/login/',methods=["GET","POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # 获取form表单数据
        data = form.data
        print(data.get("account"))
        admin = Admin.query.filter_by(name=data['account']).first()
        print(admin.name, admin.password)
        if not admin.check_pw(data['password']):
            flash("输入密码不正确")
            return redirect(url_for("admin.login"))
        # if generate_password_hash(data['password']) == admin.password:
        session['admin'] = data["account"]
        return redirect(url_for("admin.index"))
    return render_template("hdmin/login.html", form=form)


@admin.route('/loginout/')
@admin_login_req
def loginout():
    del session["admin"]   # 登出时删除session
    return redirect(url_for("admin.login"))


@admin.route('/password/')
@admin_login_req
def password():
    return render_template("hdmin/password.html")



# 标签添加
@admin.route('/tag/add/',methods=["GET","POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        print("niha1")
        tag_data = form.data
        print(tag_data['tag_name'])
        tag = Tag.query.filter_by(name=tag_data["tag_name"]).first()
        print(tag)
        if tag:
            flash("标签已存在，请不要重复添加","err")
            return redirect(url_for("admin.tag_add"))
        tags = Tag(name=tag_data["tag_name"])
        db.session.add(tags)
        flash("添加成功","ok")
        db.session.commit()
        return redirect(url_for("admin.tag_add"))
    return render_template("hdmin/tag_add.html",form=form)


@admin.route('/tag/list/')
@admin_login_req
def tag_list():
    tags = Tag.query.all()
    return render_template("hdmin/tag_list.html",tags=tags)

@admin.route('/tag/delete/<id>')
@admin_login_req
def tag_delete(id):
    tag = Tag.query.filter_by(id=id).first()
    print(tag)
    if tag:
        db.session.delete(tag)   # 删除标签
        db.session.commit()
        flash("删除成功")
    return redirect(url_for("admin.tag_list"))



@admin.route('/movie/add/')
@admin_login_req
def movie_add():
    return render_template("hdmin/movie_add.html")


@admin.route('/movie/list/')
@admin_login_req
def movie_list():
    return render_template("hdmin/movie_list.html")


@admin.route('/preview/add/')
@admin_login_req
def preview_add():
    return render_template("hdmin/preview_add.html")


@admin.route('/preview/list/')
@admin_login_req
def preview_list():
    return render_template("hdmin/preview_list.html")


@admin.route('/user/list/')
@admin_login_req
def user_list():
    return render_template("hdmin/user_list.html")


@admin.route('/user/view/')
@admin_login_req
def user_view():
    return render_template("hdmin/user_view.html")


@admin.route('/comment/')
@admin_login_req
def comment_list():
    return render_template("hdmin/comment_list.html")


@admin.route('/moviecol/list/')
@admin_login_req
def moviecol_list():
    return render_template("hdmin/moviecol_list.html")


@admin.route('/oplog/list/')
@admin_login_req
def oplog_list():
    return render_template("hdmin/oplog_list.html")


@admin.route('/adminloginlog/list/')
@admin_login_req
def adminloginlog_list():
    return render_template("hdmin/adminloginlog_list.html")


@admin.route('/uesrloginlog/list/')
@admin_login_req
def userloginlog_list():
    return render_template("hdmin/userloginlog_list.html")


@admin.route('/auth/add/')
@admin_login_req
def auth_add():
    return render_template("hdmin/auth_add.html")


@admin.route('/auth/list/')
@admin_login_req
def auth_list():
    return render_template("hdmin/auth_list.html")


@admin.route('/role/add/')
@admin_login_req
def role_add():
    return render_template("hdmin/role_add.html")


@admin.route('/role/list/')
@admin_login_req
def role_list():
    return render_template("hdmin/role_list.html")


@admin.route('/admin/add/')
@admin_login_req
def admin_add():
    return render_template("hdmin/admin_add.html")


@admin.route('/admin/list/')
@admin_login_req
def admin_list():
    return render_template("hdmin/admin_list.html")