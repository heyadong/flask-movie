from flask import render_template, url_for, redirect,flash ,request,session
from . import admin
from .forms import LoginForm
from app.models import Admin
from werkzeug.security import generate_password_hash
from functools import wraps
# def admin_login_req(func):
#     @wraps(func)
#     def decr
#
#

@admin.route('/', methods=["GET", "POST"])
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
    return render_template("hdmin/login.html",form=form)


@admin.route('/loginout/')
def loginout():
    return redirect(url_for("admin.login"))


@admin.route('/password/')
def password():
    return render_template("hdmin/password.html")


@admin.route('/tag/add/')
def tag_add():
    return render_template("hdmin/tag_add.html")


@admin.route('/tag/list/')
def tag_list():
    return render_template("hdmin/tag_list.html")


@admin.route('/movie/add/')
def movie_add():
    return render_template("hdmin/movie_add.html")


@admin.route('/movie/list/')
def movie_list():
    return render_template("hdmin/movie_list.html")


@admin.route('/preview/add/')
def preview_add():
    return render_template("hdmin/preview_add.html")


@admin.route('/preview/list/')
def preview_list():
    return render_template("hdmin/preview_list.html")


@admin.route('/user/list/')
def user_list():
    return render_template("hdmin/user_list.html")


@admin.route('/user/view/')
def user_view():
    return render_template("hdmin/user_view.html")


@admin.route('/comment/')
def comment_list():
    return render_template("hdmin/comment_list.html")


@admin.route('/moviecol/list/')
def moviecol_list():
    return render_template("hdmin/moviecol_list.html")


@admin.route('/oplog/list/')
def oplog_list():
    return render_template("hdmin/oplog_list.html")


@admin.route('/adminloginlog/list/')
def adminloginlog_list():
    return render_template("hdmin/adminloginlog_list.html")


@admin.route('/uesrloginlog/list/')
def userloginlog_list():
    return render_template("hdmin/userloginlog_list.html")


@admin.route('/auth/add/')
def auth_add():
    return render_template("hdmin/auth_add.html")


@admin.route('/auth/list/')
def auth_list():
    return render_template("hdmin/auth_list.html")


@admin.route('/role/add/')
def role_add():
    return render_template("hdmin/role_add.html")


@admin.route('/role/list/')
def role_list():
    return render_template("hdmin/role_list.html")


@admin.route('/admin/add/')
def admin_add():
    return render_template("hdmin/admin_add.html")


@admin.route('/admin/list/')
def admin_list():
    return render_template("hdmin/admin_list.html")