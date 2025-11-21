from flask import Blueprint, render_template, jsonify

schedule_bp = Blueprint('schedule_bp', __name__)

# Dummy schedule data
SCHEDULE = [
    {"day": "Mon", "date": 10, "meds": [
        {"name": "Aspirin",   "dose": "100mg", "time": "08:00 AM", "status": "Taken"},
        {"name": "Lisinopril","dose": "10mg",  "time": "02:00 PM", "status": "Upcoming"},
    ]},
    {"day": "Tue", "date": 11, "meds": [
        {"name": "Aspirin", "dose": "100mg", "time": "08:00 AM", "status": "Upcoming"},
    ]},
]

@schedule_bp.route('/calendar')
def calendar():
    # medicationcalendar.html
    return render_template('medicationcalendar.html', schedule=SCHEDULE)


@schedule_bp.route('/api/schedule')
def api_schedule():
    return jsonify(SCHEDULE)
