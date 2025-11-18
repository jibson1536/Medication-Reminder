from flask import Blueprint, render_template, request

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/')
def home():
    return render_template('index.html')

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    return render_template('index.html')

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    return render_template('signup.html')

@auth_bp.route('/welcome')
def welcome():
    return render_template('welcome.html')
