from home.app import app
from home.forms import LoginForm
from home.models import *
from flask import render_template, flash, redirect, url_for, request
from flask_login import login_user, current_user, login_required, logout_user
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
        user = User.query.filter_by(username=loginform.username.data).first()
        if user and check_password_hash(user.password_hash, loginform.password.data):
            login_user(user, remember=loginform.remember.data)
            next_page = request.args.get("next")
            return redirect(next_page) if next_page else redirect(url_for("home"))
        else:
            flash("Login Unsuccessful. Please check email and password", "danger")
    return render_template("login.html", loginform=loginform)

@app.route("/logout", methods=["GET", "POST"])
@login_required
def logout():
    logout_user()
    flash("You Have Been Logged Out!  Thanks For Stopping By...")
    return redirect(url_for("login"))

#region YouTube routes
YT_BASE="/yt"
@app.route(YT_BASE, methods=["GET", "POST"])
@login_required
def yt():
    flash("YoutTube not implemented yet...")
    return redirect(url_for("home"))
#endregion

# @app.route("/journal", methods=["GET", "POST"])
# @login_required
# def journal():
#     flash("Journal not implemented yet...")
#     return redirect(url_for("home"))

# @app.route("/recipe", methods=["GET", "POST"])
# @login_required
# def recipes():
#     flash("Recipes not implemented yet...")
#     return redirect(url_for("home"))

# @app.route("/static", methods=["GET", "POST"])
# @login_required
# def static_files():
#     flash("static files not implemented yet...")
#     return redirect(url_for("home"))