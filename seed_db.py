"""
Database seeding script to populate sample lawyers.
Run this script once to add sample lawyers to the database.
"""
from app import create_app
from app.models import User, LawyerProfile, ISSUE_CATEGORIES
from app.extensions import db

# Sample lawyers data - richer profiles, ensuring strong coverage in each category
SAMPLE_LAWYERS = [
    {
        "name": "Sarah Mitchell",
        "email": "sarah.mitchell@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Harassment", "Workplace Discrimination"],
        "experience": "With over 12 years of experience in employment law, I specialize in harassment and discrimination cases. I've successfully represented over 220 clients and have a strong record of negotiated settlements.",
        "rating": 4.8,
        "profile_picture": "lawyer1.jpg",
        "education": "J.D., Harvard Law School",
        "age": 39,
        "city": "New York, NY",
        "case_success_rate": 0.89,
    },
    {
        "name": "Michael Chen",
        "email": "michael.chen@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Domestic Violence", "Family Disputes"],
        "experience": "Dedicated family law attorney with 15 years of experience, focusing on domestic violence, custody disputes, and protective orders.",
        "rating": 4.9,
        "profile_picture": "lawyer2.jpg",
        "education": "J.D., Stanford Law School",
        "age": 42,
        "city": "San Francisco, CA",
        "case_success_rate": 0.92,
    },
    {
        "name": "Emily Rodriguez",
        "email": "emily.rodriguez@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Property Issues", "Fraud"],
        "experience": "Real estate and fraud litigation specialist helping clients resolve complex property disputes and title fraud.",
        "rating": 4.7,
        "profile_picture": "lawyer3.jpg",
        "education": "J.D., University of Texas School of Law",
        "age": 37,
        "city": "Austin, TX",
        "case_success_rate": 0.87,
    },
    {
        "name": "David Thompson",
        "email": "david.thompson@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Workplace Discrimination", "Harassment"],
        "experience": "Employment law expert with 18 years of experience in high-stakes harassment and discrimination litigation.",
        "rating": 4.9,
        "profile_picture": "lawyer4.jpg",
        "education": "J.D., Columbia Law School",
        "age": 45,
        "city": "Chicago, IL",
        "case_success_rate": 0.91,
    },
    {
        "name": "Jennifer Park",
        "email": "jennifer.park@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Family Disputes", "Domestic Violence"],
        "experience": "Family law attorney providing trauma-informed representation in divorce, custody, and domestic violence matters.",
        "rating": 4.8,
        "profile_picture": "lawyer5.jpg",
        "education": "J.D., NYU School of Law",
        "age": 38,
        "city": "Seattle, WA",
        "case_success_rate": 0.88,
    },
    {
        "name": "Robert Williams",
        "email": "robert.williams@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Property Issues"],
        "experience": "Property law specialist with two decades of experience in landlord-tenant disputes and boundary conflicts.",
        "rating": 4.6,
        "profile_picture": "lawyer6.jpg",
        "education": "J.D., University of Michigan Law School",
        "age": 50,
        "city": "Detroit, MI",
        "case_success_rate": 0.84,
    },
    {
        "name": "Lisa Anderson",
        "email": "lisa.anderson@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Fraud", "Property Issues"],
        "experience": "Criminal and civil fraud attorney focused on financial crimes, investment scams, and real estate fraud.",
        "rating": 4.7,
        "profile_picture": "lawyer7.jpg",
        "education": "J.D., UCLA School of Law",
        "age": 41,
        "city": "Los Angeles, CA",
        "case_success_rate": 0.86,
    },
    {
        "name": "James Martinez",
        "email": "james.martinez@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Harassment"],
        "experience": "Civil rights attorney representing clients in harassment and hostile work environment claims.",
        "rating": 4.5,
        "profile_picture": "lawyer8.jpg",
        "education": "J.D., Georgetown University Law Center",
        "age": 36,
        "city": "Washington, DC",
        "case_success_rate": 0.83,
    },
    {
        "name": "Amanda Foster",
        "email": "amanda.foster@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Domestic Violence", "Family Disputes"],
        "experience": "Domestic violence advocate supporting survivors through safety planning, restraining orders, and custody.",
        "rating": 4.9,
        "profile_picture": "lawyer9.jpg",
        "education": "J.D., Boston University School of Law",
        "age": 40,
        "city": "Boston, MA",
        "case_success_rate": 0.93,
    },
    {
        "name": "Christopher Lee",
        "email": "christopher.lee@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Workplace Discrimination"],
        "experience": "Employment discrimination attorney handling complex cases involving bias and wrongful termination.",
        "rating": 4.8,
        "profile_picture": "lawyer10.jpg",
        "education": "J.D., University of Chicago Law School",
        "age": 43,
        "city": "Houston, TX",
        "case_success_rate": 0.9,
    },
    {
        "name": "Patricia Brown",
        "email": "patricia.brown@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Fraud"],
        "experience": "White-collar crime and fraud attorney focusing on complex corporate and securities fraud.",
        "rating": 4.7,
        "profile_picture": "lawyer11.jpg",
        "education": "J.D., University of Pennsylvania Carey Law School",
        "age": 47,
        "city": "Philadelphia, PA",
        "case_success_rate": 0.88,
    },
    {
        "name": "Daniel Taylor",
        "email": "daniel.taylor@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Family Disputes"],
        "experience": "Family law mediator and litigator helping families resolve disputes with minimal conflict.",
        "rating": 4.8,
        "profile_picture": "lawyer12.jpg",
        "education": "J.D., Northwestern Pritzker School of Law",
        "age": 49,
        "city": "Minneapolis, MN",
        "case_success_rate": 0.9,
    },
    {
        "name": "Olivia Sanders",
        "email": "olivia.sanders@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Harassment", "Domestic Violence"],
        "experience": "Attorney focused on harassment and intimate partner violence, with strong courtroom advocacy skills.",
        "rating": 4.9,
        "profile_picture": "lawyer13.jpg",
        "education": "J.D., Duke University School of Law",
        "age": 35,
        "city": "Raleigh, NC",
        "case_success_rate": 0.92,
    },
    {
        "name": "Noah Patel",
        "email": "noah.patel@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Property Issues", "Workplace Discrimination"],
        "experience": "Attorney handling workplace disputes and complex property co-ownership conflicts.",
        "rating": 4.6,
        "profile_picture": "lawyer14.jpg",
        "education": "J.D., Vanderbilt Law School",
        "age": 39,
        "city": "Nashville, TN",
        "case_success_rate": 0.85,
    },
    {
        "name": "Sophia Garcia",
        "email": "sophia.garcia@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Fraud", "Harassment"],
        "experience": "Experienced litigator in financial fraud and harassment cases with multilingual client support.",
        "rating": 4.8,
        "profile_picture": "lawyer15.jpg",
        "education": "J.D., University of California, Berkeley",
        "age": 34,
        "city": "San Diego, CA",
        "case_success_rate": 0.9,
    },
    {
        "name": "Ethan Hughes",
        "email": "ethan.hughes@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Domestic Violence", "Family Disputes"],
        "experience": "Family lawyer focused on safety planning, custody arrangements, and survivor-centered representation.",
        "rating": 4.7,
        "profile_picture": "lawyer16.jpg",
        "education": "J.D., University of Virginia School of Law",
        "age": 38,
        "city": "Richmond, VA",
        "case_success_rate": 0.88,
    },
    {
        "name": "Mia Rossi",
        "email": "mia.rossi@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Property Issues", "Family Disputes"],
        "experience": "Attorney handling property division and asset tracing in complex family law cases.",
        "rating": 4.6,
        "profile_picture": "lawyer17.jpg",
        "education": "J.D., University of Toronto Faculty of Law",
        "age": 37,
        "city": "Toronto, ON",
        "case_success_rate": 0.86,
    },
    {
        "name": "Liam Johnson",
        "email": "liam.johnson@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Workplace Discrimination", "Fraud"],
        "experience": "Attorney focusing on discrimination, whistleblower retaliation, and corporate fraud investigations.",
        "rating": 4.7,
        "profile_picture": "lawyer18.jpg",
        "education": "J.D., University of Edinburgh School of Law",
        "age": 44,
        "city": "Denver, CO",
        "case_success_rate": 0.88,
    },
    {
        "name": "Hannah Kim",
        "email": "hannah.kim@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Harassment", "Workplace Discrimination", "Fraud"],
        "experience": "Cross-practice attorney working on harassment, discrimination, and internal fraud investigations.",
        "rating": 4.9,
        "profile_picture": "lawyer19.jpg",
        "education": "J.D., London School of Economics",
        "age": 33,
        "city": "London, UK",
        "case_success_rate": 0.93,
    },
    {
        "name": "Omar Rahman",
        "email": "omar.rahman@lawconnect.com",
        "password": "lawyer123",
        "expertise": ["Family Disputes", "Domestic Violence"],
        "experience": "Family dispute resolution specialist with extensive mediation and trial experience.",
        "rating": 4.8,
        "profile_picture": "lawyer20.jpg",
        "education": "J.D., University of Sydney Law School",
        "age": 41,
        "city": "Sydney, AU",
        "case_success_rate": 0.9,
    },
]


def seed_database():
    """Seed the database with sample lawyers."""
    app = create_app()
    
    with app.app_context():
        print("Seeding database with sample lawyers...")
        
        added_count = 0
        skipped_count = 0
        
        for lawyer_data in SAMPLE_LAWYERS:
            # Check if user already exists
            existing_user = User.query.filter_by(email=lawyer_data["email"]).first()
            if existing_user:
                print(f"Skipping {lawyer_data['name']} - already exists")
                skipped_count += 1
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
                profile_picture=lawyer_data["profile_picture"],
                education=lawyer_data.get("education", ""),
                age=lawyer_data.get("age", 0),
                city=lawyer_data.get("city", ""),
                case_success_rate=lawyer_data.get("case_success_rate", 0.0),
            )
            db.session.add(profile)
            print(f"Added lawyer: {lawyer_data['name']}")
            added_count += 1
        
        db.session.commit()
        print(f"\n✓ Successfully added {added_count} new lawyers!")
        if skipped_count > 0:
            print(f"  (Skipped {skipped_count} lawyers that already exist)")
        
        # Verify lawyers exist
        total_lawyers = LawyerProfile.query.count()
        print(f"\nTotal lawyers in database: {total_lawyers}")


if __name__ == "__main__":
    seed_database()


