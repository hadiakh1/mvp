import os
from flask import Flask

from .extensions import db, login_manager
from .config import Config
from .routes import main_bp


def create_app():
    # Get the root directory (parent of app/)
    root_dir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
    
    app = Flask(
        __name__,
        instance_relative_config=False,
        template_folder=os.path.join(root_dir, "templates"),
        static_folder=os.path.join(root_dir, "static"),
    )
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        # Register blueprints
        app.register_blueprint(main_bp)

        # Create database tables if they don't exist
        db.create_all()

    return app



