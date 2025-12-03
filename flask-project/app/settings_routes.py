from flask import (
    Blueprint,
    render_template,
    jsonify,
    request,
    redirect,
    url_for,
    flash,
)
from flask_login import current_user
from datetime import datetime
from .database import mongo

# Blueprint must match __init__.py
settings_bp = Blueprint('settings_bp', __name__)

# ---- MongoDB collections ----
user_settings_collection = mongo.db.user_settings        # for reminder sound + settings
email_changes_collection = mongo.db.email_changes        # logs email changes
delete_account_logs_collection = mongo.db.delete_account_logs  # NEW: logs delete-account actions


# ---------- MAIN SETTINGS PAGE ----------
# URL = /settings/  (because of url_prefix="/settings")
@settings_bp.route('/')
def settings():
    return render_template('settings.html')


# ---------- SECURITY PAGE ----------
@settings_bp.route('/security')
def security():
    return render_template('security.html')


# ---------- SIMPLE API (optional demo) ----------
@settings_bp.route('/api')
def api_settings():
    user_id = str(current_user.get_id()) if current_user.is_authenticated else "demo-user"
    doc = user_settings_collection.find_one({"user_id": user_id}) or {}
    return jsonify({
        "reminder_sound": doc.get("reminder_sound", "Default"),
        "notifications_enabled": doc.get("notifications_enabled", True),
    })


# ---------- CHANGE EMAIL (writes to NEW collection: email_changes) ----------
@settings_bp.route('/change-email', methods=['GET', 'POST'])
def change_email():
    if not current_user.is_authenticated:
        flash('You must be logged in to change your email.', 'danger')
        return redirect(url_for('auth_bp.login'))

    user_id = str(current_user.get_id())

    if request.method == 'POST':
        new_email = request.form.get('new_email')

        if not new_email:
            flash('Please enter an email address.', 'danger')
            return render_template('change_email.html')

        # log the change into email_changes collection
        email_changes_collection.insert_one({
            "user_id": user_id,
            "old_email": current_user.email,
            "new_email": new_email,
            "changed_at": datetime.utcnow()
        })

        flash('Your email change has been recorded in MongoDB.', 'success')
        return redirect(url_for('settings_bp.settings'))

    return render_template('change_email.html')


# ---------- REMINDER SOUND (REAL DB CONNECTION in user_settings) ----------
@settings_bp.route('/reminder-sound', methods=['GET', 'POST'])
def reminder_sound():
    available_sounds = ['Default', 'Chime', 'Beep', 'Bell']

    user_id = str(current_user.get_id()) if current_user.is_authenticated else "demo-user"

    if request.method == 'POST':
        selected = request.form.get('sound')

        if selected not in available_sounds:
            flash('Please select a valid sound.', 'danger')
            return render_template(
                'reminder_sound.html',
                available_sounds=available_sounds,
                selected_sound=selected or 'Default'
            )

        # save selected sound in user_settings collection
        user_settings_collection.update_one(
            {"user_id": user_id},
            {"$set": {"reminder_sound": selected}},
            upsert=True
        )

        flash('Reminder sound saved.', 'success')
        return redirect(url_for('settings_bp.settings'))

    doc = user_settings_collection.find_one({"user_id": user_id})
    selected_sound = (doc or {}).get("reminder_sound", "Default")

    return render_template(
        'reminder_sound.html',
        available_sounds=available_sounds,
        selected_sound=selected_sound
    )


# ---------- PRIVACY POLICY ----------
@settings_bp.route('/privacy-policy')
def privacy_policy():
    return render_template('privacy_policy.html')


# ---------- TERMS OF SERVICE ----------
@settings_bp.route('/terms-of-service')
def terms_of_service():
    return render_template('terms_of_service.html')


# ---------- DELETE ACCOUNT (logs to NEW collection) ----------
@settings_bp.route('/delete-account', methods=['POST'])
def delete_account():
    # log the delete-account action in MongoDB
    user_id = str(current_user.get_id()) if current_user.is_authenticated else "anonymous"

    delete_account_logs_collection.insert_one({
        "user_id": user_id,
        "triggered_at": datetime.utcnow(),
        "note": "User clicked delete account (simulated)."
    })

    flash('Account deletion is simulated. Action has been logged in MongoDB.', 'info')
    return redirect(url_for('auth_bp.login'))
