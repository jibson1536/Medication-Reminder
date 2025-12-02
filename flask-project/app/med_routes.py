from flask import Blueprint, render_template, jsonify, redirect, url_for, request
from flask import request, redirect, url_for
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from app.database import mongo

med_bp = Blueprint('med_bp', __name__)


# -----------------------------
# Dashboard Page
# -----------------------------
@med_bp.route('/dashboard')
@login_required
def dashboard():
    return render_template('dashboard.html')


# -----------------------------
# Med List Page
# -----------------------------
@med_bp.route('/medlist')
@login_required
def medlist():
    return render_template('medlist.html')


# -----------------------------
# Add Medication Page
# -----------------------------
from flask import request, flash
@med_bp.route('/addmed', methods=["GET", "POST"])
@login_required
def addmed():
    if request.method == "POST":
        name = request.form.get("name")
        dose = request.form.get("dose")
        freq = request.form.get("freq")
        time = request.form.get("time")
        start_date = request.form.get("start_date")
        duration_value = int(request.form.get("duration_value"))
        duration_unit = request.form.get("duration_unit")

        if not name or not dose or not freq or not time:
            flash("All fields are required", "error")
            return redirect(url_for("med_bp.addmed"))
        from datetime import datetime

        mongo.db.medications.insert_one({
            "user_id": current_user.get_id(),
            "name": name,
            "dose": dose,
            "freq": freq,
            "time": time,
            "status": "ongoing",
            "date": datetime.now()  # Temporary until we use real scheduling

        })
        flash("Medication added successfully!", "success")
        return redirect(url_for("med_bp.dashboard"))

    return render_template("addmed.html")


# -----------------------------
# Edit Medication Page (real DB)
# -----------------------------
@med_bp.route('/editmed/<string:med_id>')
@login_required
def editmed(med_id):
    med = mongo.db.medications.find_one({"_id": ObjectId(med_id), "user_id": current_user.get_id()})
    if not med:
        return "Medication not found", 404

    med["_id"] = str(med["_id"])
    return render_template('editmed.html', med=med)


# -----------------------------
# JSON API: All medications
# -----------------------------
@med_bp.route('/api/meds')
@login_required
def api_meds():
    meds = list(mongo.db.medications.find({"user_id": current_user.get_id()}))

    # Convert ObjectId → string
    for med in meds:
        med["_id"] = str(med["_id"])

    return jsonify(meds)


# -----------------------------
# JSON API: Single med details
# -----------------------------
@med_bp.route('/api/meds/<string:med_id>')
@login_required
def api_med(med_id):
    med = mongo.db.medications.find_one({"_id": ObjectId(med_id), "user_id": current_user.get_id()})
    
    if not med:
        return jsonify({"error": "Medication not found"}), 404
    
    med["_id"] = str(med["_id"])
    return jsonify(med)


# -----------------------------
# JSON API: Dashboard Stats
# -----------------------------
@med_bp.route('/api/dashboard')
@login_required
def api_dashboard():
    from datetime import date

    user_id = current_user.get_id()
    today_str = date.today().strftime("%Y-%m-%d")

    meds = list(mongo.db.medications.find({"user_id": user_id}))
    taken_logs = list(mongo.db.taken_log.find({
        "user_id": user_id,
        "date": today_str
    }))

    # med_id is stored as STRING in taken_log
    taken_ids = {log["med_id"] for log in taken_logs}

    for med in meds:
        med["_id"] = str(med["_id"])                 # make sure it's a string
        med["status"] = "taken" if med["_id"] in taken_ids else "upcoming"

    total_today = len(meds)
    taken_today = len(taken_ids)
    upcoming = total_today - taken_today

    stats = {
        "total_today": total_today,
        "taken_today": taken_today,
        "upcoming": upcoming
    }

    return jsonify({"stats": stats, "meds": meds})

from datetime import datetime, date
from bson import ObjectId
@med_bp.route("/api/meds/<med_id>/take", methods=["POST"])
@login_required
def api_take_med(med_id):
    """Mark a medication as taken for TODAY for the current user."""
    user_id = current_user.get_id()
    today_str = date.today().strftime("%Y-%m-%d")

    # Store med_id as STRING so it matches med["_id"] after str(...)
    mongo.db.taken_log.update_one(
        {"user_id": user_id, "med_id": med_id, "date": today_str},
        {
            "$set": {
                "taken_at": datetime.utcnow(),
            }
        },
        upsert=True,
    )

    return jsonify({"ok": True})
