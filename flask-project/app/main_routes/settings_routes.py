from flask import Blueprint, render_template, request

settings_bp = Blueprint('settings_bp', __name__, url_prefix='/settings')

@settings_bp.route('/', methods=['GET', 'POST'])
def settings():
    if request.method == 'POST':
        theme = request.form.get('theme')
        return "Settings updated!"
    return render_template('settings.html')

@settings_bp.route('/security', methods=['GET', 'POST'])
def security():
    if request.method == 'POST':
        current_password = request.form.get('current_password')
        return "Password updated!"
    return render_template('security.html')
