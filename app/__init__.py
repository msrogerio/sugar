from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import config

db = SQLAlchemy()

def create_applicaton():
    app = Flask(__name__)
    app.config.from_object(config)
    db.init_app(app)

    from .main import main as main_bp
    app.register_blueprint(main_bp)

    return app