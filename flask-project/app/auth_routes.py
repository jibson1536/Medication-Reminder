from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth_bp', __name__)

# Login Page
@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('login.html')   # or index.html if that's your login page

# Signup Page
@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

# Welcome / Landing Page
@auth_bp.route('/welcome')
def welcome():
    return render_template('welcome.html')
