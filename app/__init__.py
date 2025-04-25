from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

application = Flask(__name__)
application.config.from_object(Config)
db = SQLAlchemy(application)
migrate = Migrate(application, db)

csrf = CSRFProtect(application)
login = LoginManager(application)
login.login_view = 'login'  # Redirect to login page if not authenticated

print("Using SECRET_KEY:", application.config['SECRET_KEY'])

from app import routes, models