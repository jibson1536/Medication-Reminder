from flask import Flask
from app.main import main as main_blueprint

def create_app():
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(main_blueprint)

    return app