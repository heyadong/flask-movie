from . import admin
from flask import render_template,url_for,request
from app.models import User
from app import db


@admin.route('/admin',methods=["GET","POST"])
def login():
    if request.method == 'POST':
        try:
            username = request.form.get('name')
            password = request.form.get('pw')
            user_info = User(username=username,pw=password)
            db.session.add(user_info)
            db.session.commit()
        except:
            pass
    return render_template("login_admin.html")
