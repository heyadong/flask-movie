from flask import Blueprint
admin = Blueprint('admin',__name__) #定义蓝图
import app.admin.views