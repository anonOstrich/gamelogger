from application import db
from application.models import Base

class Game(Base):
    name = db.Column(db.String(255), nullable=False)
    developer = db.Column(db.String(255), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    year = db.Column(db.Integer, nullable=False) 

    reviews = db.relationship("Review", backref="game", lazy=True)

    def __init__(self, name, developer, description, year):
        self.name = name
        self.developer = developer
        self.description = description
        self.year = year
        
        

