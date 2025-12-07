"""
Script to seed the database on Render deployment.
This runs automatically via the release command in Procfile.
"""
import os
import sys

def seed_on_deploy():
    """Seed the database if it's empty (first deployment)."""
    try:
        from app import create_app
        from app.models import User, LawyerProfile
        from app.extensions import db
        
        app = create_app()
        
        with app.app_context():
            # Ensure tables exist
            db.create_all()
            
            # Check if database is empty
            user_count = User.query.count()
            lawyer_count = LawyerProfile.query.count()
            
            print(f"Current database state: {user_count} users, {lawyer_count} lawyers")
            
            # Only seed if database is empty (first deployment)
            if lawyer_count == 0:
                print("Database is empty. Seeding with sample lawyers...")
                # Import and run seed function
                from seed_db import seed_database
                seed_database()
                print("✓ Database seeded successfully!")
            else:
                print("Database already has data. Skipping seed.")
                
    except Exception as e:
        print(f"Error during database seeding: {e}")
        import traceback
        traceback.print_exc()
        # Don't fail deployment if seeding fails - exit with 0
        print("Warning: Seeding failed, but deployment will continue.")
        sys.exit(0)


if __name__ == "__main__":
    seed_on_deploy()

