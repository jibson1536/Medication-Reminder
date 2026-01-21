from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_user, logout_user, UserMixin
from bson.objectid import ObjectId
from datetime import datetime, timedelta
import bcrypt
import jwt
import os
from functools import wraps

from .database import mongo
from . import login_manager

auth_bp = Blueprint("auth_bp", __name__)

JWT_SECRET = os.getenv("JWT_SECRET", "super_secret_jwt_key")
JWT_EXPIRES_HOURS = int(os.getenv("JWT_EXPIRES_HOURS", 1))


class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data["_id"])
        self.name = user_data.get("name", "")
        self.email = user_data.get("email", "")
        self.password_hash = user_data.get("password")


@login_manager.user_loader
def load_user(user_id):
    try:
        user = mongo.db.users.find_one({"_id": ObjectId(user_id)})
        return User(user) if user else None
    except Exception:
        return None


def _normalize_hash(stored_hash):
    """
    MongoDB might store password hash as:
    - bytes (correct)
    - bson Binary (behaves like bytes)
    - str (wrong / legacy)
    - "b'...'" string (wrong / legacy)
    This converts it safely to bytes or returns None.
    """
    if stored_hash is None:
        return None

    # bytes / Binary
    if isinstance(stored_hash, (bytes, bytearray)):
        return bytes(stored_hash)

    # string cases
    if isinstance(stored_hash, str):
        s = stored_hash.strip()

        # case: "b'...'"
        if (s.startswith("b'") and s.endswith("'")) or (s.startswith('b"') and s.endswith('"')):
            s = s[2:-1]

        # bcrypt hashes are ASCII-safe, so encoding is fine
        return s.encode("utf-8")

    # unknown type
    return None


# ---------- SIGNUP ----------
@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = (request.form.get("name") or "").strip()
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        if not name or not email or not password:
            flash("Please fill in all fields.", "error")
            return redirect(url_for("auth_bp.signup"))

        existing = mongo.db.users.find_one({"email": email})
        if existing:
            flash("Email already in use.", "error")
            return redirect(url_for("auth_bp.signup"))

        hashed_pw = bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())

        mongo.db.users.insert_one({
            "name": name,
            "email": email,
            "password": hashed_pw,           # ✅ store as bytes
            "created_at": datetime.utcnow()
        })

        flash("Account created successfully! Please log in.", "success")
        return redirect(url_for("auth_bp.login"))

    return render_template("signup.html")


# ---------- LOGIN (Session + JWT) ----------
@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = (request.form.get("email") or "").strip().lower()
        password = request.form.get("password") or ""

        user = mongo.db.users.find_one({"email": email})

        if not user:
            flash("Invalid email or password", "error")
            return render_template("login.html")

        stored_hash = _normalize_hash(user.get("password"))

        if not stored_hash:
            # This means the user doc has a broken password format in MongoDB
            flash("This account password is corrupted. Please sign up again or reset the user in DB.", "error")
            return render_template("login.html")

        try:
            ok = bcrypt.checkpw(password.encode("utf-8"), stored_hash)
        except ValueError:
            # "Invalid salt" ends here cleanly
            flash("This account password is corrupted. Please sign up again (or delete this user in MongoDB).", "error")
            return render_template("login.html")

        if ok:
            login_user(User(user), remember=True)  # ✅ remember helps keep session stable

            payload = {
                "user_id": str(user["_id"]),
                "email": user["email"],
                "exp": datetime.utcnow() + timedelta(hours=JWT_EXPIRES_HOURS)
            }
            token = jwt.encode(payload, JWT_SECRET, algorithm="HS256")

            if request.is_json:
                return jsonify({"token": token})

            return redirect(url_for("med_bp.dashboard"))

        flash("Invalid email or password", "error")
        return render_template("login.html")

    return render_template("login.html")


@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth_bp.login"))


# ---------- API JWT PROTECTION ----------
def token_required(f):
    @wraps(f)
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