# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired,ValidationError
from app.models import Admin


class LoginForm(FlaskForm):
    account = StringField(
        label="账号",
        # vallidators 验证器
        validators=[
        DataRequired("请输入账号"),
        ],
        description="账号",
         # render_kw 前端渲染表单样式
        render_kw={"class": "form-control","placeholder": "请输入账号"}
        )
    password = PasswordField(
        label="密码",
        description="密码",
        validators=[
            DataRequired("请输入密码")
        ],
        render_kw={
            "class": "form-control",
            "placeholder": "请输入密码",
        }
    )  #，此处不要添加逗号会导致渲染错误
    submit = SubmitField(
        "登陆",
        render_kw={"class": "btn btn-primary btn-block btn-flat"}
    )

    # 再点击登陆时检测账号是否存在（点击登陆触发）
    def validate_account(self,field):
        account = field.data
        admin = Admin.query.filter_by(name=account).count()
        if admin == 0:
            raise ValidationError("账号不存在")


# 添加标签表单
class TagForm(FlaskForm):
    tag_name = StringField(
        label="标签",
        validators=[DataRequired("请输入标签名称")],
        description="tag's name",
        render_kw={
            "class": "form-control",
            "placeholder":"请输入标签名称！"
        }
    )
    add = SubmitField(
        "添加",
        render_kw={"class":"btn btn-primary"}
    )

