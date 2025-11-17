from flask import Blueprint, render_template, request, redirect, url_for

auth_bp = Blueprint('auth_bp', __name__)

@auth_bp.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        # Collect form data
        email = request.form.get('email')
        password = request.form.get('password')
        return redirect(url_for('onboarding_bp.onboarding'))
    return render_template('signup.html')

@auth_bp.route('/welcome')
def welcome():
    return render_template('welcome.html')
