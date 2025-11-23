from flask import Flask, redirect, url_for

def create_app():
    app = Flask(__name__)

    # Import blueprints
    from .auth_routes import auth_bp
    from .onboarding_routes import onboarding_bp
    from .med_routes import med_bp
    from .schedule_routes import schedule_bp
    from .notify_routes import notify_bp
    from .profile_routes import profile_bp
    from .settings_routes import settings_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(onboarding_bp)
    app.register_blueprint(med_bp)
    app.register_blueprint(schedule_bp)
    app.register_blueprint(notify_bp)
    app.register_blueprint(profile_bp)
    app.register_blueprint(settings_bp)

    # ⭐ DEFAULT ROUTE
    @app.route("/")
    def index():
        return redirect(url_for("auth_bp.welcome"))

    return app
