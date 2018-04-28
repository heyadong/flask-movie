# coding:utf-8
from flask import flash, render_template,url_for,request,redirect,session
from . import blog
from app.models import User, Movie,Comment,Tag
from app import db, app
from .forms import Userlogin_form,User_Regist,UserInfo,EditPassword,CommentForm
from werkzeug.security import generate_password_hash
from functools import wraps
from ..admin.views import change_file
from werkzeug.utils import secure_filename
import os, stat

def login_req(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        if session.get('user'):
            print(session.get('user'))
            return func(*args, **kwargs)
        return redirect(url_for('blog.login'))
    return wrap


# @blog.route("/", methods=["GET", "POST"])
# def index():
#     movies = Movie.query.all()
#     print("nihao1", movies)
#     return render_template('index.html',movies=movies)

# 首页
@blog.route('/index/')
def index1():
    tags = Tag.query.all()
    tag = request.args.get('tag')
    star = request.args.get('star',1)
    time = request.args.get('time',0)
    play_nums = request.args.get('play_num',0)
    comments = request.args.get('comments',0)
    p = dict(
        tag=tag,
        star=star,
        time=time,
        play_nums=play_nums,
        comments=comments
    )
    if tag is None:
        movies = Movie.query.all()
    else:
        movies = Movie.query.join(
             Tag,
             Movie.tag_id == Tag.id
        ).filter(
            Tag.name == tag
        ).all()
    # tag_id = Tag.query.joinfilter_by(name=tag).first().id
    # movies = Movie.query.filter_by(tag_id=tag_id).all()
    return render_template('home/index.html',movies=movies,tags=tags,p=p)

# 登陆
@blog.route('/login/',methods=["GET", "POST"])
# 注意路由使用'/login/'
def login():
    form = Userlogin_form()
    if form.validate_on_submit():
        data = form.data
        user = User.query.filter_by(name=data["username"]).first()
        if user.check_pw(data['password']):
            session['user'] = user.id
            print(session.get('user'))
            return redirect(url_for("blog.index1"))
        flash('密码不正确','error')
        return redirect(url_for('blog.login'))
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
    del session['user']
    print(session.get('user'))
    return redirect(url_for("blog.login"))


# 更改密码
@blog.route('/password/',methods=["GET","POST"])
@login_req
def password():
    form = EditPassword()
    user = User.query.filter_by(id=session['user']).first()
    if form.validate_on_submit():
        data = form.data
        user.password = generate_password_hash(data['newpw'])
        db.session.add(user)
        db.session.commit()
        flash("修改密码成功",'ok')
        return redirect(url_for('blog.login'))
    return render_template('home/password.html',form=form)


# 用户中心页面
@blog.route('/user/',methods=["GET","POST"])
@login_req
def user():
    form = UserInfo()
    usersname = User.query.with_entities(User.name).all()
    form.face_photo.validators=[]  # 修改face_photo验证
    form.email.validators=[]
    users = User.query.filter_by(id=session['user']).first()
    if request.method == 'GET':
        form.name.data = users.name
        form.info.data = users.info
        form.phone.data = users.phone
    if form.validate_on_submit():
        data = form.data
        if (data['name'],) in usersname:
            flash('昵称已存在', 'error')
        if form.face_photo.data.filename:
            filename = secure_filename(form.face_photo.data.filename)  # 不支持中文名称
            face_photo = change_file(filename)
            users.pagra = face_photo
            if not os.path.exists(app.config['PHOTO_FACE']):
                os.mkdir(app.config["PHOTO_FACE"])
                os.chmod(app.config["PHOTO_FACE"], stat.S_IRWXU)  # stat.S_IRWXU 读写权限
            form.face_photo.data.save(app.config['PHOTO_FACE']+face_photo)
        users.name = data['name']
        users.info = data['info']
        users.phone = data['phone']
        db.session.add(users)
        db.session.commit()
        flash('修改成功', 'ok')
        return redirect(url_for('blog.user'))
    return render_template('home/user.html', form=form, users=users)




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
@blog.route('/search/<int:page>')
def search(page):
    if page is None:
        page = 1
    key = request.args.get('key','')
    movie = Movie.query.filter(
        Movie.title.ilike('%' + key + '%')).paginate(
        page=page,
        per_page=1
    )
    counts = len(list(movie.items))
    return render_template("home/search.html",data=movie,key=key,counts=counts)


# 播放
@blog.route('/play/<int:id>-<int:page>',methods=['GET','POST'])
def play(id, page=None):
    form = CommentForm()
    if page is None:
        page = 1
    if request.method == "GET":
        movie = Movie.query.filter_by(id=id).first()
        user = User.query.filter_by(id=session.get('user')).first()
        comments = Comment.query.filter_by(movie_id=id).paginate(
            page=page,
            per_page=3
        )
    if form.validate_on_submit():
        data = form.data
        content = data['content']
        movie_id = id
        user_id = session['user']
        comment = Comment(content=content, user_id=user_id, movie_id=movie_id)
        db.session.add(comment)
        db.session.commit()
        flash('评论成功','ok')
        return redirect(url_for('blog.play', id=id, page=1))
    return render_template("home/play.html", movie=movie, user=user, form=form, comments=comments)