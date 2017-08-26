from flask import Flask
from flask_mysqldb import MySQL


# Create instance of flask class
app = Flask(__name__)

from app import views

# Config MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'  # MySQL root password
app.config['MYSQL_DB'] = 'blogapp'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'  # Return the database as a dict

# Config secret key
app.secret_key = '123456'

# Initialize MYSQL
mysql = MySQL(app)
