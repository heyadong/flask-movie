from flask import render_template, url_for, redirect, flash, request, session
from . import admin
from .forms import LoginForm, TagForm,MovieForm
from app.models import Admin, Tag,Movie
from app import db,app
from werkzeug.security import generate_password_hash
from functools import wraps
from werkzeug.utils import secure_filename
import os
import uuid
import datetime

# 登陆限制。使用装饰器进行登陆限制
def admin_login_req(func):
    @wraps(func)
    def decrated_fuc(*args, **kwargs):
        if session.get("admin") is None:
            return redirect(url_for("admin.login"))
        return func(*args, **kwargs)
    return decrated_fuc


def change_file(filename):
    file_info = os.path.splitext(filename)
    # 使用随机字符串对视频连接加密
    filename = datetime.datetime.now().strftime("%Y%m%d%H%M%S")+str(uuid.uuid4().hex)+file_info[-1]
    return filename

# session.permanent = True  session 过期时间设置，没有设置过期时间默认浏览器关闭session过期


@admin.route('/', methods=["GET", "POST"])
@admin_login_req
def index():
    return render_template("hdmin/index.html")


@admin.route('/login/', methods=["GET", "POST"])
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
    del session["admin"]  # 登出时删除session
    return redirect(url_for("admin.login"))


@admin.route('/password/')
@admin_login_req
def password():
    return render_template("hdmin/password.html")


# 标签添加
@admin.route('/tag/add/', methods=["GET", "POST"])
@admin_login_req
def tag_add():
    form = TagForm()
    if form.validate_on_submit():
        tag_data = form.data
        tag = Tag.query.filter_by(name=tag_data["tag_name"]).first()
        if tag:
            flash("标签已存在，请不要重复添加", "err")
            return redirect(url_for("admin.tag_add"))
        tags = Tag(name=tag_data["tag_name"])
        db.session.add(tags)
        flash("添加成功", "ok")
        db.session.commit()
        return redirect(url_for("admin.tag_add"))
    return render_template("hdmin/tag_add.html", form=form)


@admin.route('/tag/list/<int:page>', methods=["GET"])
@admin_login_req
def tag_list(page=None):
    if page is None:
        page = 1
    tags = Tag.query.order_by(Tag.add_time.desc())  # 查询tags并按照添加时间降序排序
    page_data = tags.paginate(page=page, per_page=2)    # paginate 对进行分页page 参数表示页数，per_page 每页显示数量
    return render_template("hdmin/tag_list.html", page_data=page_data)

# 标签删除
@admin.route('/tag/delete/<id>')
@admin_login_req
def tag_delete(id):
    tag = Tag.query.filter_by(id=id).first()
    print(tag)
    if tag:
        db.session.delete(tag)  # 删除标签
        db.session.commit()
        flash("删除成功")
    return redirect(url_for("admin.tag_list"))

# 查询标签
@admin.route('/tag/query/<name>')
@admin_login_req
def tag_query(name):
    tag = Tag.query.filter(Tag.name.ilike("%"+name+"%")).order_by(Tag.add_time.desc())
    tag_date = tag.paginate(page=1, per_page=1)
    return render_template("hdmin/tag_list.html", page_data=tag_date)



# 电影添加
@admin.route('/movie/add/',methods=["GET","POST"])
@admin_login_req
def movie_add():
    movie_form = MovieForm()
    if movie_form.validate_on_submit():
        movie_data = movie_form.data
        file_url = secure_filename(movie_form.url.data.filename)  # 使用安全文件名称secure_filename()
        file_log = secure_filename(movie_form.pages.data.filename)
        # 判断是否存在保存文件的目录，不存在就创建，并授权读写
        if not os.path.exists(app.config['UP_DIR']):
            os.makedirs(app.config["UP_DIR"])
            os.chmod(app.config["UP_DIR"], "rw")
        url = change_file(file_url)
        page = change_file(file_log)
        print(url, page)
        # 保存文件到目录
        movie_form.url.data.save(app.config["UP_DIR"]+url)
        movie_form.pages.data.save(app.config["UP_DIR"]+page)
        movie = Movie(
            title=movie_data['title'],
            url=url,
            info=movie_data["info"],
            logo=page,
            star=int(movie_data['star']),
            palynum=0,
            commentnum=0,
            tag_id=int(movie_data['tag_id']),
            area=movie_data['area'],
            relase_time=movie_data['release_time'],
            lenth=movie_data['length']
        )
        db.session.add(movie)
        db.session.commit()
        flash("添加电影成功","ok")
        return redirect(url_for("admin.movie_add"))
    return render_template("hdmin/movie_add.html",form=movie_form)

# 电影列表
@admin.route('/movie/list/<int:page>')
@admin_login_req
def movie_list(page=None):
    if page is None:
        page=1
    movies = Movie.query.order_by(Movie.add_time.desc())
    movie_data = movies.paginate(page=page, per_page=2)
    return render_template("hdmin/movie_list.html",movie_data=movie_data)

# 电影删除
@admin.route('/movie/del/<int:id>')
@admin_login_req
def movie_del(id):
    movie = Movie.query.filter_by(id=id).first_or_404()
    db.session.delete(movie)
    db.session.commit()
    flash("删除电影成功")
    return redirect(url_for("admin.movie_list", page=1))

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
