"""
Diagnostic script to check lawyers in the database.
Run this on Render to see what lawyers exist and their expertise.
"""
from app import create_app
from app.models import LawyerProfile, User, ISSUE_CATEGORIES
from app.extensions import db

app = create_app()

with app.app_context():
    total_lawyers = LawyerProfile.query.count()
    print(f"\n{'='*60}")
    print(f"TOTAL LAWYERS IN DATABASE: {total_lawyers}")
    print(f"{'='*60}\n")
    
    if total_lawyers == 0:
        print("❌ NO LAWYERS FOUND! Run: python seed_db.py")
    else:
        print("✓ Lawyers found. Here are the first 10:\n")
        for profile in LawyerProfile.query.limit(10).all():
            print(f"  • {profile.user.name}")
            print(f"    Email: {profile.user.email}")
            print(f"    Expertise: {profile.expertise_categories}")
            print(f"    Rating: {profile.rating}")
            print()
        
        # Check coverage by category
        print(f"\n{'='*60}")
        print("LAWYER COVERAGE BY CATEGORY:")
        print(f"{'='*60}\n")
        for category in ISSUE_CATEGORIES:
            count = LawyerProfile.query.filter(
                LawyerProfile.expertise_categories.like(f"%{category}%")
            ).count()
            print(f"  {category:30s}: {count:3d} lawyers")
        
        print(f"\n{'='*60}")

