from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, UserMixin
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import bcrypt
import jwt
import os

from .database import mongo
from . import login_manager  # ← FIXED IMPORT

auth_bp = Blueprint("auth_bp", __name__)

JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_jwt_key")
JWT_EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", 1))


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.name = user_data["name"]
        self.email = user_data["email"]
        self.password_hash = user_data["password"]


@login_manager.user_loader
def load_user(user_id):
    user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
    return User(user) if user else None


# ---------- SIGNUP ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        password = request.form.get("password")

        existing = mongo.db.users.find_one({"email": email})
        if existing:
            flash("Email already in use", "error")
            return redirect(url_for("auth_bp.signup"))

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw,
        })

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth_bp.login"))

    return render_template("signup.html")


# ---------- LOGIN (Session + JWT) ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = mongo.db.users.find_one({"email": email})

        if user and bcrypt.checkpw(password.encode("utf-8"), user["password"]):
            login_user(User(user))  # Flask session login

            # CREATE JWT TOKEN (for API)
            payload = {
                "user_id": str(user["_id"]),
                "email": user["email"],
                "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRES_HOURS)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

            # If it's an API request (JSON expected)
            if request.is_json:
                return jsonify({"token": token})

            # Browser login → redirect to dashboard:
            return redirect(url_for("med_bp.dashboard"))

        flash("Invalid email or password", "error")

    return render_template("login.html")


# ---------- API JWT PROTECTION ----------
def token_required(f):
    def wrapper(*args, **kwargs):
        auth_header = request.headers.get("Authorization", "")
        if not auth_header.startswith("Bearer "):
            return jsonify({"message": "Token missing"}), 401

        token = auth_header.split(" ")[1]
        try:
            payload = jwt.decode(token, JWT_SECRET, algorithms=["HS256"])
            request.user = payload
        except jwt.InvalidTokenError:
            return jsonify({"message": "Invalid or expired token"}), 401

        return f(*args, **kwargs)
    wrapper.__name__ = f.__name__
    return wrapper


@auth_bp.route("/profile_api")
@token_required
def profile_api():
    return jsonify({
        "message": "Authenticated via JWT!",
        "user": request.user
    })
@auth_bp.route("/welcome")
def welcome():
    return render_template("welcome.html")

