from flask import Blueprint

main = Blueprint('main', __name__)

# Import route files so Flask loads them
from app.main import routes_dashboard
from app.main import routes_medication
from app.main import routes_profile
from app.main import routes_settings
