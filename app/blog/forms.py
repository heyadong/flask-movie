from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired,Email,Length
from app.models import User


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

    def validator_user(self, field):
        username = field.data
        user = User.query.filter_by(name=username).count()
        if user == 0:
            raise ValidationError("错误的用户名")


# 用户登陆表单
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
        print(phone)
        user = User.query.filter_by(phone=phone).count()
        if user != 0:
            raise ValidationError('手机号已被注册，请更改')



