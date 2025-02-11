# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager



# Initialize db as an instance of SQLAlchemy
db = SQLAlchemy()

def create_app():
    app = Flask(__name__)

    # Load environment variables from the .env file
    load_dotenv()

    # App configuration
    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
    jwt = JWTManager(app)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from app.blueprints.admin_blueprint import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')

    from app.blueprints.users_blueprint import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.blueprints.teams_blueprint import teams_bp
    app.register_blueprint(teams_bp, url_prefix='/teams')

    from app.blueprints.admin_blueprint import admin_blueprint
    app.register_blueprint(admin_blueprint, url_prefix='/admin')

    # Add correct prefix if needed
    # Create all tables inside the app context
    with app.app_context():
        db.create_all()

    return app
