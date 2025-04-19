from flask import Flask
from config import Config

application = Flask(__name__)
application.config.from_object(Config)
print("Using SECRET_KEY:", application.config['SECRET_KEY'])

import app.routes 