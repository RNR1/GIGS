from flask import Flask

from .models import User, Gig
from .routes.auth import auth
from .routes.main import main

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    app.register_blueprint(main)
    app.register_blueprint(auth)

    return app