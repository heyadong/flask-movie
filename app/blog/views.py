# coding:utf-8
from flask import render_template,url_for,request
from . import blog

@blog.route("/",methods=["GET","POST"])
def index():
    print(request.args.get('name'))
    return render_template('index.html')

