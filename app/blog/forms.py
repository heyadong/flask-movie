from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, ValidationError,FileField,TextAreaField
from wtforms.validators import DataRequired,Email,Length
from flask import session
from werkzeug.security import check_password_hash
from app.models import User

# 用户登陆表单
class Userlogin_form(FlaskForm):
    username = StringField(
        label="用户",
        description="用户",
        validators=[DataRequired("请输入用户名/邮箱/手机号码")],
        render_kw={"class": "form-control input-lg", "placeholder": "用户名/邮箱/手机号码"})
    password = PasswordField(
        label="密码",
        description="密码",
        validators=[DataRequired("请输入密码")],
        render_kw={"class": "form-control input-lg", "placeholder": "密码"})
    submit = SubmitField(
        "登陆",
        render_kw={"class": "btn btn-lg btn-success btn-block"}
    )

    def validate_username(self, field):
        username = field.data
        user = User.query.filter_by(name=username).count()
        if user == 0:
            raise ValidationError("错误的用户名")


# 用户注册表单
class User_Regist(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[DataRequired("请输入昵称")],
        description="name",
        render_kw={
            'id':'input_name',
            'class':'form-control input-lg',
            'placeholder':'昵称',

        }
    )
    email = StringField(
        label='邮箱',
        validators=[Email()],
        description="email",
        render_kw={
            'id':'input_email',
            'type':'email',
            'class':"form-control input-lg",
            'placeholder': '邮箱',
        }
    )
    phone = StringField(
        label="手机",
        validators=[Length(min=11,max=11,message="请输入长度为11位的手机号")],
        description="请输入手机号",
        render_kw={
            'id': 'input_phone',
            'class':'form-control input-lg',
            'placeholder':'手机',

        }
    )
    password = PasswordField(
        label='密码',
        validators=[DataRequired('请输入密码')],
        description='password',
        render_kw={
            'id' : "input_password",
            'class':'form-control input-lg',
            'placeholder':'密码',
        }
    )
    repeat_password = PasswordField(
        label='确认密码',
        validators=[DataRequired('请输入密码')],
        description='password',
        render_kw={
            'id': "input_repassword",
            'class':'form-control input-lg',
            'placeholder':'确认密码',
            'onblur':"check_password()",
        }
    )
    confirm = SubmitField(
        '确认',
        render_kw={
            "class":"btn btn-lg btn-success btn-block",
        }
    )
    # validate_+字段名（self,field）固定方法
    def validate_phone(self,field):
        #  手机号重复验证
        phone = field.data
        user = User.query.filter_by(phone=phone).count()
        if user != 0:
            raise ValidationError('手机号已被注册，请更改')

    def validate_name(self,filed):
        '''用户名重复验证'''
        user = User.query.filter_by(name=filed.data).count()
        if user != 0:
            raise ValidationError('用户名已注册')

class UserInfo(FlaskForm):
    name = StringField(
        label='昵称',
        validators=[DataRequired('请输入昵称')],
        description='name',
        render_kw={
            'class':'form-control',
            'placeholder' :"昵称",
            }
    )
    email = StringField(
        label="邮箱",
        validators=[Email('请输入正确的邮箱地址')],
        description="email",
        render_kw={
            'class':'form-control',
            'placeholder':'邮箱',
            'type':'email'
        }
    )
    phone = StringField(
        label='手机',
        validators=[DataRequired('请输入昵称')],
        description='name',
        render_kw={
            'class':'form-control',
            'placeholder' :"手机",
            }
    )
    face_photo = FileField(
        label='头像',
        validators=[DataRequired("请选择头像")],
        render_kw={
            'class':'form-control  glyphicon glyphicon-open',
            'style':'margin-top:6px',
        }
    )
    info = TextAreaField(
        label="简介",
        validators=[DataRequired('请输入简介')],
        description="simple_info",
        render_kw={
            'class': 'form-control',
            'rows': "10",
            'id': "input_info"
        }

    )
    submit = SubmitField(
        '保存修改',
        render_kw={
            'class': "btn btn-success glyphicon glyphicon-saved",
            'style':"margin-top:6px"
        }
    )

# 密码修改表单


class EditPassword(FlaskForm):
    oldpw = StringField(
        label="旧密码",
        validators=[],
        description="old password",
        render_kw={
            'id':'input_oldpw',
            'class':'form-control',
            'placeholder':'旧密码',
            'type': 'password'
        }
    )
    newpw = StringField(
        label="新密码",
        validators=[],
        description="old password",
        render_kw={
            'id':'input_oldpw',
            'class':'form-control',
            'placeholder':'新密码',
            'type': 'password'
        }
    )
    submit = SubmitField(
        "修改密码",
        render_kw={
            'class':"btn btn-success"
        }
    )

    def validate_oldpw(self,field):
        # 验证输入旧密码是否正确
        old_pw = field.data
        pw = User.query.filter_by(id=session['user']).first().password
        if not check_password_hash(pw, old_pw):
            raise ValidationError("输入的原密码不正确")

# 评论表单
class CommentForm(FlaskForm):
    content = TextAreaField(
        label='内容',
        description='content',
        validators=[DataRequired('评论')],
        render_kw={
            'id':"input_content"
        }
    )
    submitc = SubmitField(
        '提交评论',
        render_kw={
            'class':"btn btn-success glyphicon glyphicon-edit",
            'id':"btn-sub"
        }
    )

