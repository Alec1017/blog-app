from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate


# Create instance of flask class
app = Flask(__name__)

# Get configuration settings
app.config.from_object('config')

# Initialize db
db = SQLAlchemy(app)

# Initialize migration
migrate = Migrate(app, db)

from app import views, models
