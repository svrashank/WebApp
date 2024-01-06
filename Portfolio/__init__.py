from flask_sqlalchemy import SQLAlchemy 
from flask import Flask
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from werkzeug.debug import DebuggedApplication

app = Flask(__name__)

app.config['SECRET_KEY'] = '33ee76435e33c8d672bc482b26616d20'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)

bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'users.sign_in'
login_manager.login_message_category ='info'

from Portfolio.users.routes import users_blueprint 
from Portfolio.projects.routes import projects_blueprint
from Portfolio.qualifications.routes import qualifications_blueprint
from Portfolio.skills.routes import skills_blueprint
from Portfolio.main.routes import main

app.register_blueprint(users_blueprint)
app.register_blueprint(projects_blueprint)
app.register_blueprint(qualifications_blueprint)
app.register_blueprint(skills_blueprint)
app.register_blueprint(main)