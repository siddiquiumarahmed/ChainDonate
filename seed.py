from app import create_app, db
from app.models import Charity

app = create_app()

with app.app_context():

    if Charity.query.first():
        print("Charities already exist.")
    else:
        charities = [
            Charity(
                name="Red Cross",
                description="Provides emergency assistance and disaster relief.",
                category="Disaster Relief"
            ),
            Charity(
                name="UNICEF",
                description="Supports children through education, health, and protection.",
                category="Children"
            ),
            Charity(
                name="Save the Children",
                description="Improves the lives of children around the world.",
                category="Children"
            ),
            Charity(
                name="WWF",
                description="Protects wildlife and the environment.",
                category="Environment"
            ),
            Charity(
                name="Doctors Without Borders",
                description="Provides medical care where it is needed most.",
                category="Healthcare"
            )
        ]

        db.session.add_all(charities)
        db.session.commit()

        print("Charities added successfully!")