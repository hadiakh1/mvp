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
        
        # Auto-migrate or seed database on first deployment (Railway/Render)
        # Only runs if database is empty
        try:
            from .models import LawyerProfile
            lawyer_count = LawyerProfile.query.count()
            if lawyer_count == 0:
                # Database is empty
                # Only run in production (when DATABASE_URL is set)
                if os.environ.get("DATABASE_URL"):
                    # Seed database with sample lawyers
                    print("Database is empty. Seeding with sample lawyers...")
                    try:
                        from seed_db import seed_database
                        seed_database()
                        print("✓ Database seeded successfully!")
                    except Exception as e:
                        print(f"Warning: Could not seed database: {e}")
        except Exception as e:
            # Silently fail - don't break app startup
            pass

    return app



