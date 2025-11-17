from flask import Blueprint, render_template, request

notify_bp = Blueprint('notify_bp', __name__, url_prefix='/notifications')

@notify_bp.route('/')
def notifications():
    return render_template('notifications.html')

@notify_bp.route('/settings', methods=['GET', 'POST'])
def notification_settings():
    if request.method == 'POST':
        reminder_time = request.form.get('reminder_time')
        return "Settings saved!"
    return render_template('notificationsettings.html')
