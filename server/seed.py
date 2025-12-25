from app import app
from models import db, Hero, Power, HeroPower
from random import choice 

def seed_database():

    with app.app_context():
        print("Clearing existing data...")
        HeroPower.query.delete()
        Power.query.delete()

        db.session.commit()

        print("Creating heroes...")

        heroes = [
            Hero(name="Kamala Khan", super_name="Ms. Marvel"),
            Hero(name="Doreen Green", super_name="Squirrel Girl"),
            Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
            Hero(name="Janet Van Dyne", super_name="The Wasp"),
            Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
            Hero(name="Carol Danvers", super_name="Captain Marvel"),
            Hero(name="Jean Grey", super_name="Dark Phoenix"),
            Hero(name="Ororo Munroe", super_name="Storm"),
            Hero(name="Kitty Pryde", super_name="Shadowcat"),
            Hero(name="Elektra Natchios", super_name="Elektra")
        ]

        db.session.add_all(heroes)
        db.session.commit()

        print(f"Created {len(heroes)} heroes")

        print("Creating powers...")

        power = [
            Power(
                name="super strength",
                description="gives the wielder super-human strengths"
            ),
            Power(
                name="flight",
                description="gives the wielder the ability to fly through the skies at supersonic speed"
            ),
            Power(
                name="super human senses",
                description="allows the wielder to use her senses at a super-human level"
            ),
            Power(
                name="elasticity",
                description="can stretch the human body to extreme lengths"
            ),
            Power(
                name="telekinesis",
                description="allows the wielder to move objects with their mind at incredible speeds"
            ),
            Power(
                name="energy projection",
                description="grants the ability to project powerful energy beams from the body"
            ),
            Power(
                name="telepathy",
                description="enables communication through thoughts and reading of other minds"
            ),
            Power(
                name="weather manipulation",
                description="provides control over atmospheric conditions and weather patterns"
            ),
            Power(
                name="phasing",
                description="allows the user to pass through solid matter by shifting molecular structure"
            ),
            Power(
                name="enhanced combat skills",
                description="provides mastery of various martial arts and hand-to-hand combat techniques"
            )
        ]

        