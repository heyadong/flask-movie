from . import admin
from flask import render_template,url_for,request
from app.models import Role
from app import db


@admin.route('/',methods=["GET","POST"])
def login():
    role = Role(name="superadmin", auths="")
    db.session.add(role)
    db.session.commit()
    return render_template("login_admin.html")
