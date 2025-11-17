from flask import Blueprint, render_template, request

profile_bp = Blueprint('profile_bp', __name__)

@profile_bp.route('/profile', methods=['GET', 'POST'])
def profile():
    if request.method == 'POST':
        full_name = request.form.get('full_name')
        return "Profile updated!"
    return render_template('profile.html')
