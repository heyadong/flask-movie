from flask_wtf import FlaskForm
from wtforms import SubmitField, StringField, PasswordField, ValidationError
from wtforms.validators import DataRequired
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

    def validator_user(self,field):
        username = field.data
        user = User.query.filter_by(name=username).count()
        if user == 0:
            raise ValidationError("错误的用户名")