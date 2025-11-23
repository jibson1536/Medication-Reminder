from flask import Blueprint, render_template, jsonify

settings_bp = Blueprint('settings_bp', __name__)

SETTINGS_DATA = {
    "notifications_enabled": True,
    "reminder_sound": "Default",
}

@settings_bp.route('/settings')
def settings():
    return render_template('settings.html', settings=SETTINGS_DATA)

@settings_bp.route('/security')
def security():
    return render_template('security.html')


@settings_bp.route('/api/settings')
def api_settings():
    return jsonify(SETTINGS_DATA)
