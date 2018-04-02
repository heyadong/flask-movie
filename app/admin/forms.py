# coding:utf-8
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,FileField,TextAreaField,SelectField,DateField
from flask_wtf.file import FileRequired
from wtforms.validators import DataRequired, ValidationError
from app.models import Admin, Tag

tags = Tag.query.all()
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


# 电影添加表单
class MovieForm(FlaskForm):
    title = StringField(
        label="片名",
        validators=[DataRequired("请输入片名")],
        description="movie's title",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片名！"
        }
    )
    url = FileField(
        label="文件",
        validators=[FileRequired("请上传文件")],
        description="file",
    )
    info = TextAreaField(
        label="简介",
        validators=[DataRequired("请输入简介")],
        description="infos",
        render_kw={
            "class": "form-control",
            "rows": 10
        }
    )
    pages = FileField(
        label="封面",
        validators=[DataRequired("请上传封面")],
        description="file",
    )
    star = SelectField(
        label="星级",
        validators=[DataRequired("请选择星级")],
        coerce=int,
        choices=[(m,str(n)+"星") for m in range(1, 6) for n in range(1, 6) if m==n],
        description="星级",
        render_kw={
            "class": "form-control"
        }
    )
    tag_id = SelectField(
        label="标签",
        validators=[DataRequired("请选择星级")],
        coerce=int,
        choices=[(v.id, v.name) for v in tags],
        description="标签",
        render_kw={
            "class": "form-control"
        }
    )
    area = StringField(
        label="地区",
        validators=[DataRequired("请输入地区")],
        description="area",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入地区！"
        }
    )
    length = StringField(
        label="片长",
        validators=[DataRequired("请输入片长")],
        description="length",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入片长！"
        }
    )
    release_time = StringField(
        label="上映时间",
        validators=[DataRequired("请输入上映时间")],

        description="release_time",
        render_kw={
            "class": "form-control",
            "placeholder": "请输入上映时间",
            "id": "input_release_time"
        }
    )
    add = SubmitField(
        "添加",
        render_kw={
            "class": "btn btn-primary"
        }
    )
