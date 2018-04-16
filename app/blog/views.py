# coding:utf-8
from flask import render_template,url_for,request,redirect,session
from . import blog
from app.models import User
from app import db
from .forms import Userlogin_form,User_Regist
from werkzeug.security import generate_password_hash
from functools import wraps

def login_req(func):
    @wraps(func)
    def wrap(*args,**kwargs):
        if session.get('user'):
            return func(*args,**kwargs)
        return redirect(url_for('blog.login'))
    return wrap


@blog.route("/", methods=["GET", "POST"])
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


# 登陆
@blog.route('/login/',methods=["GET", "POST"])
# 注意路由使用'/login/'
def login():
    form = Userlogin_form()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["username"]).first()
        if user.check_pw(data['password']):
            session['user'] = user.uuid
            return redirect(url_for("blog.index1"))
    return render_template('home/login.html', form=form)

# 注册
@blog.route('/register/',methods=['GET','POST'])
def register():
    form = User_Regist()
    if form.validate_on_submit():
        data = form.data
        user = User(name=data['name'],
                    password=generate_password_hash(data['password']),
                    phone=data['phone'],
                    )
        db.session.add(user)
        db.session.commit()
        return render_template('home/success_regist.html')
    return render_template('home/register.html',form=form)


# 登出
@blog.route('/logout/')
def logout():
    # redirect()重定向到登陆页面
    return redirect(url_for("blog.login"))


# 更改密码
@blog.route('/password/')
def password():
    return render_template('home/password.html')


# 用户中心页面
@blog.route('/user/')
def user():
    return render_template('home/user.html')


# 首页
@blog.route('/index/')
def index1():
    return render_template('home/index.html')


# 评论页面
@blog.route('/comment/')
def comment():
    return render_template('home/comment.html')


# 电影收藏
@blog.route('/moviecol/')
def moviecol():
    return render_template('home/moviecol.html')


# 登陆日志
@blog.route('/loginlog/')
def loginlog():
    return render_template('home/loginlog.html')


@blog.route('/animation/')
# 首页轮播页面
def animation():
    return render_template("home/animation.html")


# 搜索
@blog.route('/search/')
def search():
    return render_template("home/search.html")

# 播放
@blog.route('/play/')
def play():
    return render_template("home/play.html")