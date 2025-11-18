from flask import Blueprint, render_template

schedule_bp = Blueprint('schedule_bp', __name__)

@schedule_bp.route('/calendar')
def calendar():
    return render_template('medicationcalendar.html')
