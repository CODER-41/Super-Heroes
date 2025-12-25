from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin

metadata = MetaData(naming_convention = {
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

class Hero(db.Model, SerializerMixin):
    
    __tablename__ = 'heroes'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    super_name = db.Column(db.String(100), nullable = False)

    hero_powers = db.relationship(
        'HeroPower',
        back_populates='hero',
        cascade='all, delete-orphan'
    )

    powers = association_proxy('hero_powers', 'power')

    serialize_rules = ('-hero_powers.hero',)

    def __repr__(self):
        return f'<Hero {self.id}: {self.name} ({self.super_name})>'
    

class Power(db.Model, SerializerMixin):
    
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)

    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(225), nullable=False)

    hero_powers = db.relationship(
        'HeroPower',
        back_populates = 'power',
        cascade='all, delete-orphan'
    )

    heroes = association_proxy('hero_powers', 'hero')

    serialize_rules = ('-hero_powers.power',)

    @validates('description')
    def validate_description(self, key, description):

        if not description:
            raise ValueError("Power description is required")
        
        if len(description) < 20:
            raise ValueError("Power description must be at least 20 characters long")
        
        return description

    def __repr__(self):
        return f'<Power {self.id}: {self.name}>'
    

class HeroPower(db.Model, SerializerMixin):

    __tablename__ = 'hero_powers'


    id = db.Column(db.Integer, primary_key = True)

    strength = db.Column(db.String(20), nullable=False)

    hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id', ondelete='CASCADE'), nullable=False)
    power_id = db.Column(db.Integer, db.ForeignKey('powers.id', ondelete='CASCADE'), nullable=False)


    hero = db.relationship('Hero', back_populates = 'hero_powers')
    power = db.relationship('Power', back_populates = 'hero_powers')

    serialize_rules = ('-hero.hero_powers', '-power.hero_powers')

    @validates('strength')
    def validate_strength(self, key, strength):

        allowed_strength = ['Strong', 'Weak', 'Average']
        if strength not in allowed_strength:
            raise ValueError(f"Strength must be one of : {', '.join(allowed_strength)}")
        return strength
    
    def __repr__(self):
        return f'<HeroPower {self.id}: Hero {self.hero_id} - Power {self.power_id} ({self.strength})>'