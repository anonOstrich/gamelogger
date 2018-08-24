from application import db
from application.genres.models import GameGenre
from application.models import Base
from sqlalchemy.sql import text
import os

class Game(Base):
    name = db.Column(db.String(200), nullable=False)
    developer = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    year = db.Column(db.Integer, nullable=False) 

    reviews = db.relationship("Review", backref="game", lazy=True)
    game_genres = db.relationship("GameGenre", backref="game", lazy=True)

    def __init__(self, name, developer, description, year):
        self.name = name
        self.developer = developer
        self.description = description
        self.year = year

    def update_genres(self, genre_ids):
        # voisiko tehdä vähemmällä tietokannan käytöllä kuin poistamalla aina kaikki? 
        GameGenre.query.filter(GameGenre.game_id == self.id).delete()
        db.session.commit()
        self.add_genres(genre_ids)



    def add_genres(self, genre_ids):
        def create_game_genre(genre_id):
            result = GameGenre()
            result.game_id = self.id
            result.genre_id = genre_id
            return result

        g_genres = map(create_game_genre, genre_ids)            
        db.session.add_all(g_genres)
        db.session.commit()

        

    @staticmethod
    def find_all_numbers_of_reviews(): 
        stmt = text("SELECT Game.id, COUNT(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.id;")
        res = db.engine.execute(stmt)        
        return {row[0]:row[1] for row in res}

    
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
    def find_all_unreviewed_games(user_id):
        stmt = text("SELECT DISTINCT Game.id, Game.name FROM Game"
                    " WHERE Game.id NOT IN (SELECT Game.id FROM Game JOIN Review ON Game.id = Review.game_id"
                    " WHERE Review.account_id = :user_id); "
                      ).params(user_id=user_id)

        res=db.engine.execute(stmt)
        return [{"id":row[0], "name":row[1]} for row in res]
        
        
        

