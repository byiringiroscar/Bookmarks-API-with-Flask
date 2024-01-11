from flask import Flask
import os
from src.database import db
from src.auth import auth
from flask_jwt_extended import JWTManager

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config['DEBUG'] = True
    if test_config is None:
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            SQLALCHEMY_DATABASE_URI=os.environ.get("SQLALCHEMY_DB_URI"),
            SQLALCHEMY_TRACK_MODIFICATIONS=False,
            JWT_SECRET_KEY=os.environ.get("JWT_SECRET_KEY"),
        )
    else:
        app.config.from_mapping(test_config)
    db.app=app
    db.init_app(app)

    JWTManager(app)

    with app.app_context():
        db.create_all()  # Create tables only if they don't exist
    app.register_blueprint(auth)
    # app.register_blueprint(bookmarks)
    
    return app