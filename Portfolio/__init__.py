from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)

app.config['SECRET_KEY'] = '33ee76435e33c8d672bc482b26616d20'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'sign_in'
login_manager.login_message_category ='info'

from Portfolio import routes