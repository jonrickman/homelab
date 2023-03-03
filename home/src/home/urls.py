from home.app import app
from home.forms import LoginForm
from home.models import *
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user
from flask_httpauth import HTTPBasicAuth
from werkzeug.security import check_password_hash

basicAuth = HTTPBasicAuth()

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("home"))
    
    loginform = LoginForm()
    if loginform.validate_on_submit():
        test_user = user_factory.find_user(loginform.username.data)
        print(test_user)
        user = User.query.filter_by(username=loginform.username.data).first()
        print(f"login form: {loginform.username.data} pwd:{loginform.password.data}")
        if user and check_password_hash(user.password_hash, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", loginform=loginform)

