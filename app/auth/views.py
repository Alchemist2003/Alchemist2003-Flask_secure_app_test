from flask import Blueprint, render_template, request, redirect, session
from app.extensions import db
from app.models import User

auth_views = Blueprint("auth_views", __name__)

@auth_views.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user = User(email=request.form["email"])
        user.set_password(request.form["password"])
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")


@auth_views.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(email=request.form["email"]).first()
        if user and user.check_password(request.form["password"]):
            session["user_id"] = user.id
            return redirect("/dashboard")
    return render_template("login.html")


@auth_views.route("/logout")
def logout():
    session.clear()
    return redirect("/login")
