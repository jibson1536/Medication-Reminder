from flask import Blueprint, render_template, jsonify, request
from flask_login import login_required, current_user
from datetime import datetime, date, timedelta
from app.database import mongo

profile_bp = Blueprint("profile_bp", __name__)

# ---------- Dummy history data (optional) ----------
# You can keep this for reference, but it is NOT used by /profile/api/history anymore.
HISTORY_ITEMS = [
    {"name": "Aspirin",    "dose": "100mg", "time": "08:00 AM", "status": "Taken"},
    {"name": "Metformin",  "dose": "500mg", "time": "12:00 PM", "status": "Taken"},
    {"name": "Lisinopril", "dose": "10mg",  "time": "02:00 PM", "status": "Missed"},
]
# -----------------------------------------------


@profile_bp.route("/profile")
def profile():
    user = {
        "initials": "JD",
        "name": "John Doe",
        "email": "johndoe@example.com"
    }
    return render_template("profile.html", user=user)


@profile_bp.route("/history")
@login_required
def history():
    # History page is now populated via JS calling /profile/api/history
    return render_template("history.html")


@profile_bp.route("/api/history", methods=["GET"])
@login_required
def api_history():
    user_id = current_user.get_id()

    # last N days (default 7)
    days = int(request.args.get("days", 7))
    today = date.today()
    start_date = today - timedelta(days=days - 1)

    # get meds for user
    meds = list(mongo.db.medications.find({"user_id": user_id}))
    for m in meds:
        m["_id"] = str(m["_id"])

    # get taken logs in date range
    logs = list(mongo.db.taken_log.find({
        "user_id": user_id,
        "date": {"$gte": start_date.strftime("%Y-%m-%d"), "$lte": today.strftime("%Y-%m-%d")}
    }))

    # Build a set of (date, med_id) that were taken
    taken_set = set((log.get("date"), log.get("med_id")) for log in logs)

    # Helper: estimate times per day from freq
    def freq_per_day(freq_str):
        if not freq_str:
            return 1
        s = str(freq_str).lower()
        import re
        match = re.search(r"\d+", s)
        if match:
            n = int(match.group())
            return max(1, n)
        return 1

    # Weekly totals
    expected_week = 0
    taken_week = 0

    for i in range(days):
        d = (start_date + timedelta(days=i)).strftime("%Y-%m-%d")
        for med in meds:
            expected_week += freq_per_day(med.get("freq"))
            if (d, med["_id"]) in taken_set:
                taken_week += freq_per_day(med.get("freq"))

    missed_week = max(0, expected_week - taken_week)
    adherence = round((taken_week / expected_week) * 100) if expected_week else 0

    # Today's list
    today_str = today.strftime("%Y-%m-%d")
    now_time = datetime.now().strftime("%H:%M")

    today_items = []
    for med in meds:
        is_taken = (today_str, med["_id"]) in taken_set

        med_time = str(med.get("time") or "00:00").strip()
        missed = False
        # Only auto-miss if time is in "HH:MM" format
        if (not is_taken) and (len(med_time) == 5) and (med_time < now_time):
            missed = True

        status = "taken" if is_taken else ("missed" if missed else "upcoming")

        today_items.append({
            "med_id": med["_id"],
            "name": med.get("name", ""),
            "dose": med.get("dose", ""),
            "time": med.get("time", ""),
            "status": status
        })

    return jsonify({
        "week": {
            "adherence": adherence,
            "taken": taken_week,
            "missed": missed_week,
            "expected": expected_week
        },
        "today": today_items
    })


@profile_bp.route("/features")
def features():
    return render_template("features.html")
