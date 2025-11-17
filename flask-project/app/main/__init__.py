from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config.from_pyfile('../config.py')  # if you have config.py

    # --- Import ALL route blueprints ---
    from .auth_routes import auth_bp              # login, signup, welcome
    from .onboarding_routes import onboarding_bp  # onboarding steps 1,2,3
    from .med_routes import med_bp                # medication pages (list, add, edit, details)
    from .schedule_routes import schedule_bp      # schedule + calendar
    from .notify_routes import notify_bp          # notifications + settings
    from .profile_routes import profile_bp        # profile, history, features
    from .settings_routes import settings_bp      # settings + security

    # --- Register ALL route blueprints ---
    app.register_blueprint(auth_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(med_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(notify_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(settings_bp)

    return app
