import os

from flask import Flask
from flask_sqlalchemy import SQLAlchemy

# Initialize SQLAlchemy
db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # Configure SQLite database
    BASE_DIR = os.path.abspath(os.path.dirname(__file__))
    app.config["SQLALCHEMY_DATABASE_URI"] = (
        f'sqlite:///{os.path.join(BASE_DIR, "../database/database.db")}'
    )
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # Initialize extensions for Flask
    db.init_app(app)

    # Import and register blueprints(allows you to register the routes later)
    from app.app import app_bp
    from app.stream_routes import stream_bp

    app.register_blueprint(app_bp)
    app.register_blueprint(stream_bp)

    # Register models and create the datababase file
    with app.app_context():
        db.create_all()

    return app
