import os
from flask import Flask
from dotenv import load_dotenv
from flask_sqlalchemy import SQLAlchemy

# -----------------------------------------
# App Creation (Consider a factory function create_app() for flexibility in larger projects)
# -----------------------------------------
app = Flask(__name__)

# -----------------------------------------
# Configuration
# -----------------------------------------
load_dotenv()
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")

# -----------------------------------------
#  Database Initialisation
# -----------------------------------------
db = SQLAlchemy(app)

# -----------------------------------------
# Import Models (After app and db are initialised)
# -----------------------------------------
from app.user_model import User

# -----------------------------------------
# Blueprint Registration
# -----------------------------------------
from app.auth import auth_bp
app.register_blueprint(auth_bp)

# -----------------------------------------
# Import Routes (At the end to avoid circular dependencies)
# -----------------------------------------
from app import routes
