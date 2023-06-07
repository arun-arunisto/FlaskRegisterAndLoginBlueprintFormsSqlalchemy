from flask import Blueprint,redirect, render_template, request, url_for, flash
from .forms import RegistrationForm, LoginForm
from .models import db, User
from flask_login import login_user, current_user, login_required, logout_user

user_bp = Blueprint("user_bp", __name__,
                    template_folder="templates",
                    static_folder="static",
                    static_url_path="/userAuthentication/static")

@user_bp.route("/home")
def home():
    return render_template("home.html")

@user_bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('user_bp.login'))

@user_bp.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    print(form.validate_on_submit())
    if form.validate_on_submit():
        try:
            user = User(username=form.username.data, email=form.email.data)
            user.set_password(form.password1.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("user_bp.login"))
        except Exception as e:
            print(e)
            flash("Some Error Occured")
            return redirect(url_for("user_bp.register"))
    return render_template("register.html", form=form)

@user_bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        try:
            user = User.query.filter_by(email = form.email.data).first()
            if user is not None and user.check_password(form.password.data):
                login_user(user)
                return redirect(url_for('user_bp.home'))
            flash("Invalid email or password")
        except Exception as e:
            return redirect(url_for('user_bp.login'))
    return render_template("login.html", form=form)


