from flask import Flask
from config import Config
from app.extensions import db
from app.routes import contact_bp


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    app.register_blueprint(contact_bp)

    with app.app_context():
        db.create_all()

    return app
