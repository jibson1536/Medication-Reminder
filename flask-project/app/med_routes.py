from flask import Blueprint, render_template, jsonify, redirect, url_for, request, flash
from flask_login import login_required, current_user
from bson.objectid import ObjectId
from datetime import datetime, date
from app.database import mongo

med_bp = Blueprint("med_bp", __name__)

# Collection: stores one summary per user per day
daily_summary_collection = mongo.db.daily_summary


# -----------------------------
# Dashboard Page
# -----------------------------
@med_bp.route("/dashboard")
@login_required
def dashboard():
    return render_template("dashboard.html", user=current_user)


# -----------------------------
# Med List Page
# -----------------------------
@med_bp.route("/medlist")
@login_required
def medlist():
    return render_template("medlist.html")


# -----------------------------
# Add Medication Page
# -----------------------------
@med_bp.route("/addmed", methods=["GET", "POST"])
@login_required
def addmed():
    if request.method == "POST":
        name = request.form.get("name")
        dose = request.form.get("dose")
        freq = request.form.get("freq")
        time = request.form.get("time")
        start_date = request.form.get("start_date")  # optional
        duration_value = request.form.get("duration_value")  # unused for now
        duration_unit = request.form.get("duration_unit")    # unused for now

        if not name or not dose or not freq or not time:
            flash("All fields are required", "error")
            return redirect(url_for("med_bp.addmed"))

        mongo.db.medications.insert_one({
            "user_id": current_user.get_id(),
            "name": name,
            "dose": dose,      # e.g. "100mg"
            "freq": freq,
            "time": time,      # e.g. "08:00"
            "status": "ongoing",
            "date": datetime.utcnow()  # placeholder
        })

        flash("Medication added successfully!", "success")
        return redirect(url_for("med_bp.dashboard"))

    return render_template("addmed.html")


# -----------------------------
# Edit Medication Page (server-rendered page)
# NOTE: This page is opened via /med/editmed/<id>
# Saving is done either by:
#  - Form POST to this route (optional)
#  - OR your editmed.js calling PUT /api/meds/<id> (recommended)
# -----------------------------
@med_bp.route("/editmed/<string:med_id>", methods=["GET"])
@login_required
def editmed(med_id):
    user_id = current_user.get_id()

    med = mongo.db.medications.find_one({"_id": ObjectId(med_id), "user_id": user_id})
    if not med:
        return "Medication not found", 404

    med["_id"] = str(med["_id"])
    return render_template("editmed.html", med=med)


# -----------------------------
# JSON API: All medications
# -----------------------------
@med_bp.route("/api/meds")
@login_required
def api_meds():
    meds = list(mongo.db.medications.find({"user_id": current_user.get_id()}))
    for med in meds:
        med["_id"] = str(med["_id"])
    return jsonify(meds)


# -----------------------------
# JSON API: Single med details
# -----------------------------
@med_bp.route("/api/meds/<string:med_id>")
@login_required
def api_med(med_id):
    med = mongo.db.medications.find_one({"_id": ObjectId(med_id), "user_id": current_user.get_id()})
    if not med:
        return jsonify({"error": "Medication not found"}), 404

    med["_id"] = str(med["_id"])
    return jsonify(med)


# -----------------------------
# JSON API: Update medication (used by editmed.js)
# -----------------------------
@med_bp.route("/api/meds/<string:med_id>", methods=["PUT"])
@login_required
def api_update_med(med_id):
    user_id = current_user.get_id()
    data = request.get_json(force=True)

    name = (data.get("name") or "").strip()
    dose = data.get("dose")   # number
    unit = (data.get("unit") or "").strip()
    time = (data.get("time") or "").strip()
    freq = (data.get("freq") or "daily").strip()

    if not name or dose is None or not unit or not time:
        return jsonify({"error": "Missing required fields"}), 400

    dose_str = f"{dose}{unit}"

    result = mongo.db.medications.update_one(
        {"_id": ObjectId(med_id), "user_id": user_id},
        {"$set": {"name": name, "dose": dose_str, "time": time, "freq": freq}}
    )

    if result.matched_count == 0:
        return jsonify({"error": "Medication not found"}), 404

    return jsonify({"ok": True})


# -----------------------------
# JSON API: Delete medication (used by editmed.js)
# -----------------------------
from bson import ObjectId
from datetime import datetime

@med_bp.route("/api/meds/<string:med_id>", methods=["DELETE"])
@login_required
def api_delete_med(med_id):
    user_id = current_user.get_id()

    # 1️⃣ Find the medication first
    med = mongo.db.medications.find_one({
        "_id": ObjectId(med_id),
        "user_id": user_id
    })

    if not med:
        return jsonify({"ok": False, "error": "Medication not found"}), 404

    # 2️⃣ Add delete metadata
    med["original_id"] = str(med["_id"])
    med["deleted_at"] = datetime.utcnow()
    med["deleted_by"] = user_id

    # 3️⃣ Archive medication
    mongo.db.deleted_medications.insert_one(med)

    # 4️⃣ Archive taken logs (THIS is the part you asked about)
    logs = list(mongo.db.taken_log.find({
        "user_id": user_id,
        "med_id": med_id
    }))

    if logs:
        mongo.db.deleted_taken_log.insert_many([
            {
                **log,
                "deleted_at": datetime.utcnow(),
                "deleted_by": user_id,
                "med_original_id": med["original_id"]
            }
            for log in logs
        ])

    # 5️⃣ Delete original records
    mongo.db.medications.delete_one({
        "_id": ObjectId(med_id),
        "user_id": user_id
    })
    mongo.db.taken_log.delete_many({
        "user_id": user_id,
        "med_id": med_id
    })

    return jsonify({"ok": True})



# -----------------------------
# JSON API: Dashboard Stats + Daily Summary
# -----------------------------
@med_bp.route("/api/dashboard")
@login_required
def api_dashboard():
    user_id = current_user.get_id()
    today_str = date.today().strftime("%Y-%m-%d")

    meds = list(mongo.db.medications.find({"user_id": user_id}))
    taken_logs = list(mongo.db.taken_log.find({"user_id": user_id, "date": today_str}))

    taken_ids = {log["med_id"] for log in taken_logs}  # med_id stored as STRING

    for med in meds:
        med["_id"] = str(med["_id"])
        med["status"] = "taken" if med["_id"] in taken_ids else "upcoming"

    total_today = len(meds)
    taken_today = len(taken_ids)
    upcoming = total_today - taken_today

    stats = {
        "total_today": total_today,
        "taken_today": taken_today,
        "upcoming": upcoming
    }

    # Save/update daily summary (nice "innovation" feature)
    daily_summary_collection.update_one(
        {"user_id": user_id, "date": today_str},
        {"$set": {
            "user_id": user_id,
            "date": today_str,
            "total_today": total_today,
            "taken_today": taken_today,
            "upcoming": upcoming,
            "generated_at": datetime.utcnow()
        }},
        upsert=True
    )

    return jsonify({"stats": stats, "meds": meds})


# -----------------------------
# Mark medication as taken (API)
# -----------------------------
@med_bp.route("/api/meds/<string:med_id>/take", methods=["POST"])
@login_required
def api_take_med(med_id):
    user_id = current_user.get_id()
    today_str = date.today().strftime("%Y-%m-%d")

    mongo.db.taken_log.update_one(
        {"user_id": user_id, "med_id": med_id, "date": today_str},
        {"$set": {"taken_at": datetime.utcnow(), "date": today_str}},
        upsert=True
    )

    return jsonify({"ok": True})
