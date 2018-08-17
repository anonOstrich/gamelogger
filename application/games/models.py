from application import db
from application.models import Base
from sqlalchemy.sql import text
import os

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
            avg = row[1]
            
            if avg is None: 
                avg = ""
            # PostgreSQL:llä palautuskeskiarvojen tyyppi on decimal, jolla ei ole metodia is_integer()
            elif (not os.environ.get("HEROKU")) and avg.is_integer():
                avg = int(avg)
            else:
                avg = format(row[1], ".2f")
            review_averages[row[0]] = avg
        return review_averages
    
    @staticmethod
    def find_unreviewed_games(user_id):
        stmt = text("SELECT DISTINCT Game.id, Game.name FROM Game"
                    " WHERE Game.id NOT IN (SELECT Game.id FROM Game JOIN Review ON Game.id = Review.game_id"
                    " WHERE Review.account_id = :user_id); "
                      ).params(user_id=user_id)
        res=db.engine.execute(stmt)

        games_info = []
        for row in res:
            games_info.append({"id":row[0], "name":row[1]})
        return games_info
        
        
        

