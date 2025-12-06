"""
Quick check and fix script for localhost issues.
Run this to diagnose and fix common problems.
"""
import os
import sys

print("=" * 60)
print("LawyerConnect MVP - Localhost Diagnostic Tool")
print("=" * 60)

# Check 1: Database exists
db_path = "lawyerconnect.db"
if os.path.exists(db_path):
    print(f"✓ Database file exists: {db_path}")
else:
    print(f"✗ Database file not found: {db_path}")
    print("  The database will be created on first run.")

# Check 2: Run migration
print("\n" + "=" * 60)
print("Running database migrations...")
print("=" * 60)

try:
    import migrate_db_simple
    print("\n✓ Basic migration completed")
except Exception as e:
    print(f"\n✗ Basic migration failed: {e}")

try:
    import migrate_db_advanced
    print("✓ Advanced migration completed")
except Exception as e:
    print(f"✗ Advanced migration failed: {e}")
    print("  (This is OK if you haven't updated to the new matching algorithm yet)")

# Check 3: Test app creation
print("\n" + "=" * 60)
print("Testing app creation...")
print("=" * 60)

try:
    from app import create_app
    app = create_app()
    print("✓ App created successfully")
    
    # Test database connection
    with app.app_context():
        from app.models import User, LawyerProfile
        user_count = User.query.count()
        lawyer_count = LawyerProfile.query.count()
        print(f"✓ Database connection OK")
        print(f"  - Users: {user_count}")
        print(f"  - Lawyers: {lawyer_count}")
        
except Exception as e:
    print(f"✗ App creation failed: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print("\n" + "=" * 60)
print("Diagnostic complete!")
print("=" * 60)
print("\nIf you see errors above, fix them before running the app.")
print("To run the app: python run.py")

