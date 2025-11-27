"""
Database seeding script to populate sample lawyers.
Run this script once to add sample lawyers to the database.
"""
from app import create_app
from app.models import User, LawyerProfile, ISSUE_CATEGORIES
from app.extensions import db

# Sample lawyers data - at least one for each category
SAMPLE_LAWYERS = [
    {
        "name": "Sarah Mitchell",
        "email": "sarah.mitchell@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Harassment", "Workplace Discrimination"],
        "experience": "With over 12 years of experience in employment law, I specialize in harassment and discrimination cases. I've successfully represented over 200 clients and have a strong track record of achieving favorable outcomes.",
        "rating": 4.8,
        "profile_picture": "lawyer1.jpg"
    },
    {
        "name": "Michael Chen",
        "email": "michael.chen@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Domestic Violence", "Family Disputes"],
        "experience": "I am a dedicated family law attorney with 15 years of experience, focusing on domestic violence cases and family disputes. I provide compassionate and effective legal representation to protect my clients' rights and safety.",
        "rating": 4.9,
        "profile_picture": "lawyer2.jpg"
    },
    {
        "name": "Emily Rodriguez",
        "email": "emily.rodriguez@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Property Issues", "Fraud"],
        "experience": "Real estate and fraud litigation specialist with 10 years of experience. I help clients navigate complex property disputes and fraud cases, ensuring their interests are protected throughout the legal process.",
        "rating": 4.7,
        "profile_picture": "lawyer3.jpg"
    },
    {
        "name": "David Thompson",
        "email": "david.thompson@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Workplace Discrimination", "Harassment"],
        "experience": "Employment law expert with 18 years of experience. I've handled numerous workplace discrimination and harassment cases, helping employees secure justice and fair compensation.",
        "rating": 4.9,
        "profile_picture": "lawyer4.jpg"
    },
    {
        "name": "Jennifer Park",
        "email": "jennifer.park@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Family Disputes", "Domestic Violence"],
        "experience": "Family law attorney specializing in domestic violence and family disputes. With 14 years of experience, I provide strong advocacy and support for families in difficult situations.",
        "rating": 4.8,
        "profile_picture": "lawyer5.jpg"
    },
    {
        "name": "Robert Williams",
        "email": "robert.williams@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Property Issues"],
        "experience": "Property law specialist with 20 years of experience. I handle all types of property disputes, from landlord-tenant issues to complex real estate transactions and boundary disputes.",
        "rating": 4.6,
        "profile_picture": "lawyer6.jpg"
    },
    {
        "name": "Lisa Anderson",
        "email": "lisa.anderson@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Fraud", "Property Issues"],
        "experience": "Criminal and civil fraud attorney with 11 years of experience. I help clients recover losses from fraud and navigate complex legal issues related to financial crimes and property fraud.",
        "rating": 4.7,
        "profile_picture": "lawyer7.jpg"
    },
    {
        "name": "James Martinez",
        "email": "james.martinez@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Harassment"],
        "experience": "Civil rights attorney focusing on harassment cases. With 9 years of experience, I am committed to protecting individuals' rights and holding perpetrators accountable.",
        "rating": 4.5,
        "profile_picture": "lawyer8.jpg"
    },
    {
        "name": "Amanda Foster",
        "email": "amanda.foster@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Domestic Violence"],
        "experience": "Domestic violence advocate and attorney with 13 years of experience. I provide comprehensive legal support to survivors, including protective orders, custody matters, and criminal proceedings.",
        "rating": 4.9,
        "profile_picture": "lawyer9.jpg"
    },
    {
        "name": "Christopher Lee",
        "email": "christopher.lee@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Workplace Discrimination"],
        "experience": "Employment discrimination attorney with 16 years of experience. I represent employees who have faced discrimination based on race, gender, age, disability, and other protected characteristics.",
        "rating": 4.8,
        "profile_picture": "lawyer10.jpg"
    },
    {
        "name": "Patricia Brown",
        "email": "patricia.brown@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Fraud"],
        "experience": "White-collar crime and fraud attorney with 17 years of experience. I specialize in complex fraud cases, including identity theft, financial fraud, and corporate fraud matters.",
        "rating": 4.7,
        "profile_picture": "lawyer11.jpg"
    },
    {
        "name": "Daniel Taylor",
        "email": "daniel.taylor@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Family Disputes"],
        "experience": "Family law mediator and attorney with 19 years of experience. I help families resolve disputes through negotiation and litigation, focusing on child custody, divorce, and support matters.",
        "rating": 4.8,
        "profile_picture": "lawyer12.jpg"
    },
]


def seed_database():
    """Seed the database with sample lawyers."""
    app = create_app()
    
    with app.app_context():
        # Check if sample lawyers already exist
        existing_lawyer = User.query.filter_by(email="sarah.mitchell@lawconnect.com").first()
        if existing_lawyer:
            print("Sample lawyers already exist in the database. Skipping seed.")
            return
        
        print("Seeding database with sample lawyers...")
        
        for lawyer_data in SAMPLE_LAWYERS:
            # Check if user already exists
            existing_user = User.query.filter_by(email=lawyer_data["email"]).first()
            if existing_user:
                print(f"Skipping {lawyer_data['name']} - already exists")
                continue
            
            # Create user
            user = User(
                name=lawyer_data["name"],
                email=lawyer_data["email"],
                is_lawyer=True
            )
            user.set_password(lawyer_data["password"])
            db.session.add(user)
            db.session.flush()
            
            # Create lawyer profile
            profile = LawyerProfile(
                user_id=user.id,
                expertise_categories=",".join(lawyer_data["expertise"]),
                experience_description=lawyer_data["experience"],
                rating=lawyer_data["rating"],
                profile_picture=lawyer_data["profile_picture"]
            )
            db.session.add(profile)
            print(f"Added lawyer: {lawyer_data['name']}")
        
        db.session.commit()
        print(f"\nSuccessfully seeded {len(SAMPLE_LAWYERS)} sample lawyers!")


if __name__ == "__main__":
    seed_database()

