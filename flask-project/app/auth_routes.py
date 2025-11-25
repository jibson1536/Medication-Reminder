from flask import Blueprint, render_template, request, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash

from .database import mongo   # correct import
from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from .database import mongo

auth_bp = Blueprint("auth_bp", __name__)


@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        # 1. Find user in database
        user = mongo.db.users.find_one({"email": email})

        if user is None:
            flash("Email not found. Please sign up first.", "error")
            return redirect(url_for("auth_bp.login"))

        # 2. Check password
        if not check_password_hash(user["password"], password):
            flash("Incorrect password. Try again.", "error")
            return redirect(url_for("auth_bp.login"))

        # 3. Success → save session
        session["user_id"] = str(user["_id"])
        session["user_name"] = user["name"]

        flash("Login successful!", "success")
        return redirect(url_for("med_bp.dashboard"))

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

