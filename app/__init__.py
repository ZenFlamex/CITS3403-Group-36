from flask import Flask
from config import Config 
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_wtf.csrf import CSRFProtect
from flask_login import LoginManager

db = SQLAlchemy()
migrate = Migrate()
csrf = CSRFProtect() 
login = LoginManager()
login.login_view = 'main.login'  

# Application factory function
def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    db.init_app(app)
    migrate.init_app(app, db)
    csrf.init_app(app) 
    login.init_app(app)

    from app.routes import bp as main_blueprint 
    app.register_blueprint(main_blueprint)

    from app import models 
 
    return app