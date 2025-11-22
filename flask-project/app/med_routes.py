from flask import Blueprint, render_template, jsonify

med_bp = Blueprint('med_bp', __name__)

# ---------- Dummy data ----------
DUMMY_MEDS = [
    {"id": 1, "name": "Aspirin",     "dose": "100mg", "freq": "1× daily", "time": "08:00 AM"},
    {"id": 2, "name": "Metformin",   "dose": "500mg", "freq": "2× daily", "time": "12:00 PM"},
    {"id": 3, "name": "Lisinopril",  "dose": "10mg",  "freq": "1× daily", "time": "02:00 PM"},
    {"id": 4, "name": "Atorvastatin","dose": "20mg",  "freq": "1× daily", "time": "10:00 PM"},
]

DASHBOARD_STATS = {
    "taken_today": 3,
    "upcoming": 1,
    "total_today": 4,
    "next_med": {
        "name": "Lisinopril",
        "dose": "10mg",
        "time": "02:00 PM"
    }
}
# -------------------------------


@med_bp.route('/dashboard')
def dashboard():
    # Pass dummy stats + meds to the template
    return render_template('dashboard.html',
                           stats=DASHBOARD_STATS,
                           meds=DUMMY_MEDS)


@med_bp.route('/api/meds')
def api_meds():
    return jsonify(DUMMY_MEDS)

@med_bp.route('/addmed')
def addmed():
    return render_template('addmed.html')

@med_bp.route('/editmed/<int:med_id>')
def editmed(med_id):
    med = next((m for m in DUMMY_MEDS if m["id"] == med_id), None)
    if not med:
        return "Medication not found", 404
    return render_template('editmed.html', med=med)


@med_bp.route('/medlist')
def medlist():
    return render_template('medlist.html', meds=DUMMY_MEDS)


@med_bp.route('/details/<int:med_id>')
def details(med_id):
    med = next((m for m in DUMMY_MEDS if m["id"] == med_id), None)
    return render_template('details.html', med=med)



@med_bp.route('/medication')
def medication():
    # If you use medicationschedule.html instead, adjust name
    return render_template('medication.html', meds=DUMMY_MEDS)


# -------- JSON API endpoints (for JS fetch) ----------

@med_bp.route('/api/med/<int:med_id>')
def api_med(med_id):
    med = next((m for m in DUMMY_MEDS if m["id"] == med_id), None)
    return jsonify(med)



@med_bp.route('/api/dashboard')
def api_dashboard():
    return jsonify({
        "stats": DASHBOARD_STATS,
        "meds": DUMMY_MEDS,
    })
