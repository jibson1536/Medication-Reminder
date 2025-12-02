from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .database import mongo   # correct import
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import mongo

auth_bp = Blueprint("auth_bp", __name__)
from flask_login import UserMixin

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.password = user_data["password"]

from flask_login import login_user

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = mongo.db.users.find_one({"email": email})

        if user and check_password_hash(user["password"], password):
            login_user(User(user))
            return redirect(url_for("med_bp.dashboard"))

        flash("Invalid email or password", "error")

    return render_template("login.html")



@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        hashed_pw = generate_password_hash(password)

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw
        })

        return redirect(url_for("auth_bp.login"))

    return render_template("signup.html")


@auth_bp.route("/welcome")
def welcome():
    return render_template("welcome.html")

from bson.objectid import ObjectId
from app import login_manager

@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user) if user else None
