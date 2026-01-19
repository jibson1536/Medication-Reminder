from flask import Flask, redirect, url_for
from flask_login import LoginManager
from datetime import datetime
from dotenv import load_dotenv
import os

from .database import init_db

login_manager = LoginManager()

def create_app():
    # Load environment variables
    load_dotenv()

    app = Flask(__name__)
    
    # Use secret key from .env if available
    app.secret_key = os.getenv("SECRET_KEY", "super-secret-key")

    # Initialize MongoDB
    init_db(app)

    # Setup Flask-Login
    login_manager.init_app(app)
    login_manager.login_view = "auth_bp.login"

    # Make `now()` available in templates for time-based greetings
    app.jinja_env.globals['now'] = datetime.utcnow

    # Import Blueprints
    from .auth_routes import auth_bp
    from .onboarding_routes import onboarding_bp
    from .med_routes import med_bp
    from .schedule_routes import schedule_bp
    from .notify_routes import notify_bp
    from .profile_routes import profile_bp
    from .settings_routes import settings_bp

    # Register Blueprints
    app.register_blueprint(auth_bp, url_prefix="/auth")
    app.register_blueprint(onboarding_bp, url_prefix="/onboarding")
    app.register_blueprint(med_bp, url_prefix="/med")
    app.register_blueprint(schedule_bp, url_prefix="/schedule")
    app.register_blueprint(notify_bp, url_prefix="/notify")
    app.register_blueprint(profile_bp, url_prefix="/profile")
    app.register_blueprint(settings_bp, url_prefix="/settings")

    @app.route("/")
    def index():
        return redirect(url_for("auth_bp.login"))

    return app
