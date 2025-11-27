"""
Migration script to add rating and profile_picture columns to LawyerProfile table.
Run this once to update your existing database schema.
"""
import sqlite3
import os
from app import create_app
from app.config import Config

def migrate_database():
    """Add missing columns to LawyerProfile table if they don't exist."""
    app = create_app()
    
    with app.app_context():
        # Get database path
        db_uri = app.config['SQLALCHEMY_DATABASE_URI']
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
        else:
            print("This migration only works with SQLite databases.")
            return
        
        if not os.path.exists(db_path):
            print("Database doesn't exist yet. It will be created on first run.")
            return
        
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        
        try:
            # Check if rating column exists
            cursor.execute("PRAGMA table_info(lawyer_profile)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'rating' not in columns:
                print("Adding 'rating' column to lawyer_profile table...")
                cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN rating REAL DEFAULT 0.0")
                conn.commit()
                print("✓ Added 'rating' column")
            else:
                print("✓ 'rating' column already exists")
            
            if 'profile_picture' not in columns:
                print("Adding 'profile_picture' column to lawyer_profile table...")
                cursor.execute("ALTER TABLE lawyer_profile ADD COLUMN profile_picture VARCHAR(255) DEFAULT 'default-avatar.png'")
                conn.commit()
                print("✓ Added 'profile_picture' column")
            else:
                print("✓ 'profile_picture' column already exists")
            
            # Update existing records to have default values if they're NULL
            cursor.execute("UPDATE lawyer_profile SET rating = 0.0 WHERE rating IS NULL")
            cursor.execute("UPDATE lawyer_profile SET profile_picture = 'default-avatar.png' WHERE profile_picture IS NULL")
            conn.commit()
            
            print("\n✓ Database migration completed successfully!")
            
        except Exception as e:
            print(f"Error during migration: {e}")
            conn.rollback()
        finally:
            conn.close()


if __name__ == "__main__":
    migrate_database()

