from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    flash,
)

# Blueprint name must match what you use in url_for: "settings_bp"
settings_bp = Blueprint('settings_bp', __name__)

# Simple in-memory settings data (demo only)
SETTINGS_DATA = {
    "notifications_enabled": True,
    "reminder_sound": "Default",
    "email": "user@example.com",  # demo value
}


# ---------- MAIN SETTINGS PAGE ----------
# Full URL = /settings/  (because of url_prefix="/settings" in __init__.py)
@settings_bp.route('/')
def settings():
    return render_template('settings.html', settings=SETTINGS_DATA)


# ---------- SECURITY (existing page) ----------
# Full URL = /settings/security
@settings_bp.route('/security')
def security():
    return render_template('security.html')


# ---------- SIMPLE API ----------
# Full URL = /settings/api
@settings_bp.route('/api')
def api_settings():
    return jsonify(SETTINGS_DATA)


# ---------- CHANGE EMAIL ----------
# Full URL = /settings/change-email
@settings_bp.route('/change-email', methods=['GET', 'POST'])
def change_email():
    if request.method == 'POST':
        new_email = request.form.get('new_email')

        if not new_email:
            flash('Please enter an email address.', 'danger')
            return render_template('change_email.html')

        SETTINGS_DATA['email'] = new_email
        flash('Email updated (demo only – not real authentication).', 'success')
        return redirect(url_for('settings_bp.settings'))

    return render_template('change_email.html')


# ---------- REMINDER SOUND ----------
# Full URL = /settings/reminder-sound
@settings_bp.route('/reminder-sound', methods=['GET', 'POST'])
def reminder_sound():
    available_sounds = ['Default', 'Chime', 'Beep', 'Bell']

    if request.method == 'POST':
        selected = request.form.get('sound')
        if selected in available_sounds:
            SETTINGS_DATA['reminder_sound'] = selected
            flash('Reminder sound saved.', 'success')
            return redirect(url_for('settings_bp.settings'))
        else:
            flash('Please select a valid sound.', 'danger')

    selected_sound = SETTINGS_DATA.get('reminder_sound', 'Default')

    return render_template(
        'reminder_sound.html',
        available_sounds=available_sounds,
        selected_sound=selected_sound
    )


# ---------- PRIVACY POLICY ----------
# Full URL = /settings/privacy-policy
@settings_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


# ---------- TERMS OF SERVICE ----------
# Full URL = /settings/terms-of-service
@settings_bp.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')


# ---------- DELETE ACCOUNT ----------
# Full URL = /settings/delete-account
@settings_bp.route('/delete-account', methods=['POST'])
def delete_account():
    flash('Account deletion is simulated for this project. (No real data was removed.)', 'info')
    return redirect(url_for('auth_bp.login'))
