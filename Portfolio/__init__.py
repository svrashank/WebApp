from flask_sqlalchemy import SQLAlchemy 
from flask import Flask

app = Flask(__name__)

app.config['SECRET_KEY'] = '33ee76435e33c8d672bc482b26616d20'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)

from Portfolio import routes