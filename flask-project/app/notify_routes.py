from flask import Blueprint, render_template, jsonify

notify_bp = Blueprint('notify_bp', __name__)

# Dummy notification settings / items
NOTIFICATION_ITEMS = [
    {"name": "Medication Reminders", "enabled": True,  "desc": "Receive alerts for upcoming doses"},
    {"name": "Daily Summary",        "enabled": False, "desc": "A summary of today's medications"},
    {"name": "Missed Dose Alerts",   "enabled": True,  "desc": "Get notified when you miss a dose"},
]

@notify_bp.route('/notificationsettings')
def notificationsettings():
    return render_template('notificationsettings.html', items=NOTIFICATION_ITEMS)

@notify_bp.route('/notifications')
def notifications():
    return render_template('notifications.html', items=NOTIFICATION_ITEMS)


@notify_bp.route('/api/notifications')
def api_notifications():
    return jsonify(NOTIFICATION_ITEMS)
