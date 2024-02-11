from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os




# Make the app
app = Flask(__name__)

# Set up our database...

# How to connect (user, password, etc.)
# app.config["SQLALCHEMY_DATABASE_URI"] = "mysql://nqobile:nqobilesql@localhost/vitapulse_db"
app.config["SQLALCHEMY_DATABASE_URI"] = os.getenv("DATABASE_URI")
# Ensure we get no warnings about SQLAlchemy updates
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#  Connect SQLAlchemy to our app
db = SQLAlchemy(app)

# We need routes, but need to import routes after to avoid circular import problems...
from app import routes  # Load routing logic (endpoints, and logic)
