from . import admin
from flask import render_template, url_for, request,redirect
from app.models import Role
from app import db


@admin.route('/', methods=["GET", "POST"])
def index():
    return render_template("hdmin/index.html")


@admin.route('/login/',methods=["GET","POST"])
def login():
    return render_template("hdmin/login.html")


@admin.route('/loginout/')
def loginout():
    return redirect(url_for("admin.login"))


@admin.route('/password/')
def password():
    return render_template("hdmin/password.html")