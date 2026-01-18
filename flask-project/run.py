import os
from dotenv import load_dotenv

# 1) Read .env file
load_dotenv()

# 2) Create the Flask app
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
