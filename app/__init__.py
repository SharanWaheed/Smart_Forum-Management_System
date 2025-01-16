from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv  # Load environment variables
import os
import logging

# Import the database instance
from app.db import db  # Assuming db is defined in app.db
from app.models import admin_model  # Import all models to ensure they're registered
from app.models import users_model
from app.models import teams_model

# Initialize Migrate
migrate = Migrate()

def create_app():
    app = Flask(__name__)

    # Load environment variables from the .env file
    load_dotenv()

    # App configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')

    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)

    # Register blueprints
    from app.blueprints.admin_blueprint import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    from app.blueprints.users_blueprint import users_bp
    app.register_blueprint(users_bp, url_prefix='/users')

    from app.blueprints.teams_blueprint import teams_bp
    app.register_blueprint(teams_bp, url_prefix='/teams')
    
        

    # Create all tables
    with app.app_context():
        db.create_all()

    return app
