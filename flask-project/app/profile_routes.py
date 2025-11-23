from flask import Blueprint, render_template, jsonify

profile_bp = Blueprint('profile_bp', __name__)

# ---------- Dummy history data ----------
HISTORY_ITEMS = [
    {"name": "Aspirin",    "dose": "100mg", "time": "08:00 AM", "status": "Taken"},
    {"name": "Metformin",  "dose": "500mg", "time": "12:00 PM", "status": "Taken"},
    {"name": "Lisinopril", "dose": "10mg",  "time": "02:00 PM", "status": "Missed"},
]
# ---------------------------------------


@profile_bp.route('/profile')
def profile():
    user = {
        "initials": "JD",
        "name": "John Doe",
        "email": "johndoe@example.com"
    }
    return render_template('profile.html', user=user)


@profile_bp.route('/history')
def history():
    return render_template('history.html', history=HISTORY_ITEMS)


@profile_bp.route('/features')
def features():
    return render_template('features.html')


# -------- JSON API for history ----------
@profile_bp.route('/api/history')
def api_history():
    return jsonify(HISTORY_ITEMS)
