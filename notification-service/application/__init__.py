import config
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    environment_configuration = os.environ.get('CONFIGURATION_SETUP', 'config.ProductionConfig')
    app.config.from_object(environment_configuration)

    db.init_app(app)

    with app.app_context():
        from . import models  # must import before create_all
        from .notification_api import notification_api_blueprint
        app.register_blueprint(notification_api_blueprint)
        db.create_all()
        return app
