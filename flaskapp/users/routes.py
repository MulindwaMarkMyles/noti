from flaskapp.models import User
from flask import render_template, url_for, flash,redirect, request, Blueprint
from flaskapp import db, bcrypt
from flaskapp.users.forms import RegistrationForm, LoginForm, UpdateAccountForm, RequestResetForm, ResetPasswordForm
from flask_login import login_user, logout_user, current_user, login_required
from flaskapp.users.utils import save_picture, send_reset_email
from flaskapp.main.utils import the_device

users = Blueprint('users', __name__)

@users.route("/register",methods=["GET","POST"])
def registration():
        if current_user.is_authenticated:
                return redirect(url_for("main.home"))
        form = RegistrationForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
                user = User(username=form.username.data, email=form.email.data.strip(), password=hashed_password)
                db.session.add(user)
                db.session.commit()
                flash(f"Successfully created account for {form.username.data}!", "success")
                return redirect(url_for("users.login"))
        if the_device():
                return render_template("register-mobile.html", title="REGISTER-MOBILE", form=form,device=the_device())
        else:
                return render_template("register.html", title="REGISTER", form=form, device=the_device())

@users.route("/login", methods=["GET","POST"])
def login():
        if current_user.is_authenticated:
                return redirect(url_for("main.home"))
        form = LoginForm()
        if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data.strip()).first()
                if user and bcrypt.check_password_hash(user.password, form.password.data):
                        login_user(user, remember=form.remember.data)
                        next_page = request.args.get('next')
                        return redirect(next_page) if next_page else redirect(url_for("main.home"))
                else:
                        flash("Login unsuccessful. please check the details.", "error")
        if the_device():
                return render_template("login-mobile.html", title="LOGIN-MOBILE", form=form, device=the_device())
        else:
                return render_template("login.html", title="LOGIN", form=form,device=the_device())

@users.route("/logout")
def logout():
        logout_user()
        return redirect(url_for("users.login"))

@users.route("/account", methods=["GET","POST"])
@login_required
def account():
        form = UpdateAccountForm()
        if form.validate_on_submit():
                if form.picture.data:
                        picture_file = save_picture(form.picture.data)
                        current_user.image_file = picture_file
                current_user.username = form.username.data
                current_user.email = form.email.data
                db.session.commit()
                flash("Your account has been updated.","info")
                return redirect(url_for("users.account"))
        elif request.method == "GET":
                form.username.data = current_user.username
                form.email.data = current_user.email
        image_file = url_for('static', filename=f"images/{current_user.image_file}")
        if the_device():
                return render_template("account-mobile.html", title="ACCOUNT-MOBILE", image_file=image_file, form=form,device=the_device())
        else:
                return render_template("account.html", title="ACCOUNT", image_file=image_file, form=form, device=the_device())

@users.route("/reset_password", methods=["GET", "POST"])
def reset_password():
        if current_user.is_authenticated:
                return redirect(url_for("main.home"))
        form = RequestResetForm()
        if form.validate_on_submit():
                user = User.query.filter_by(email=form.email.data).first()
                send_reset_email(user)
                flash("An email has been sent with instructions to reset your password.","info")
                return redirect(url_for("users.login"))
        if the_device():
                return render_template("request_reset-mobile.html", title="Reset Password-Mobile", form=form, device=the_device())
        else:
                return render_template("request_reset.html", title="Reset Password", form=form, device=the_device())

@users.route("/reset_password/<token>", methods=["GET", "POST"])
def reset_token(token):
        if current_user.is_authenticated:
                return redirect(url_for("main.home"))
        user = User.verify_reset_token(token)
        if user is None:
                flash("That is an invalid token","warning")
                return redirect(url_for("users.reset_password"))
        form = ResetPasswordForm()
        if form.validate_on_submit():
                hashed_password = bcrypt.generate_password_hash(form.password.data).decode("utf-8")
                user.password = hashed_password
                db.session.commit()
                flash(f"Successfully changed password for {user.username}!", "success")
                return redirect(url_for("users.login"))
        if the_device():
                return render_template("reset-mobile.html",title="Reset Password-Mobile", form=form, device=the_device())
        else:
                return render_template("reset.html",title="Reset Password", form=form, device=the_device())