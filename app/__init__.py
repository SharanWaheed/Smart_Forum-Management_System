# app/__init__.py

from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from dotenv import load_dotenv
import os
from flask_jwt_extended import JWTManager
from flask_caching import Cache
from flask_mail import Mail



# Initialize database and cache
db = SQLAlchemy()
cache = Cache()

mail = Mail()

def create_app(config_name=None):
    app = Flask(__name__)

    # Load environment variables from .env
    load_dotenv()

    # Default configuration
    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('SQLALCHEMY_DATABASE_URI')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['JWT_SECRET_KEY'] = 'your_secret_key_here'
    app.config['PROPAGATE_EXCEPTIONS'] = True
    app.config['CACHE_TYPE'] = 'SimpleCache'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 600
 
    # Email configuration
    app.config['MAIL_SERVER'] = os.getenv("MAIL_SERVER", "smtp.gmail.com")
    app.config['MAIL_PORT'] = int(os.getenv("MAIL_PORT", 587))
    app.config['MAIL_USE_TLS'] = os.getenv("MAIL_USE_TLS", "True") == "True"
    app.config['MAIL_USE_SSL'] = os.getenv("MAIL_USE_SSL", "False") == "True"
    app.config['MAIL_USERNAME'] = os.getenv("MAIL_USERNAME")
    app.config['MAIL_PASSWORD'] = os.getenv("MAIL_PASSWORD")
    app.config['MAIL_DEFAULT_SENDER'] = os.getenv("MAIL_DEFAULT_SENDER")

    # If test mode is enabled, override the database
    if config_name == "testing":
        app.config["TESTING"] = True
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///:memory:"  # In-memory DB for tests
        app.config["WTF_CSRF_ENABLED"] = False  # Disable CSRF for testing

    # Initialize extensions
    jwt = JWTManager(app)
    cache.init_app(app)
    db.init_app(app)
    migrate = Migrate(app, db)

    # Register blueprints
    from app.blueprints.admin_blueprint import admin_bp
    from app.blueprints.users_blueprint import users_bp
    from app.blueprints.teams_blueprint import teams_bp
    from app.blueprints.project_blueprint import project_bp 
    from app.blueprints.task_blueprints import task_bp
    from app.blueprints.allocation_blueprint import allocation_bp

    app.register_blueprint(admin_bp, url_prefix='/admin')
    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(teams_bp, url_prefix='/teams')
    app.register_blueprint(project_bp)
    app.register_blueprint(task_bp)
    app.register_blueprint(allocation_bp, url_prefix="/allocations")

    # Import models to ensure database migrations detect them
    from app.models.project_model import Project
    from app.models.task_model import Task

    # Create all tables in the app context
    with app.app_context():
        db.create_all()
    mail.init_app(app)
    
    return app
