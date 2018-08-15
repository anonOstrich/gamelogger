from application import db
from application.models import Base
from sqlalchemy.sql import text

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

    @staticmethod
    def find_all_number_of_reviews(): 
        stmt = text("SELECT Game.id, COUNT(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.id;")
        res = db.engine.execute(stmt)
        
        review_numbers = {}
        
        for row in res:
            review_numbers[row[0]] = row[1]
            
        return review_numbers
    
    @staticmethod
    def find_all_averages_of_reviews():
        stmt = text("SELECT Game.id, AVG(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.id;")
        res = db.engine.execute(stmt)
        
        review_averages = {}
        
        for row in res: 
            review_averages[row[0]] = row[1]
        return review_averages
        
        
        

