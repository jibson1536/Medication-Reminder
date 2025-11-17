from flask import Blueprint, render_template

schedule_bp = Blueprint('schedule_bp', __name__, url_prefix='/schedule')

@schedule_bp.route('/')
def schedule():
    return render_template('medicationschedule.html')

@schedule_bp.route('/calendar')
def calendar():
    return render_template('medicationcalendar.html')
