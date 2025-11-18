from flask import Blueprint, render_template

notify_bp = Blueprint('notify_bp', __name__)

@notify_bp.route('/notificationsettings')
def notificationsettings():
    return render_template('notificationsettings.html')

@notify_bp.route('/notifications')
def notifications():
    return render_template('notifications.html')
