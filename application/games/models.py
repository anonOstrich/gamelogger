from application import db
from application.genres.models import GameGenre
from application.tags.models import GameTag
from application.models import Base
from sqlalchemy.sql import text
from sqlalchemy import bindparam
import os

class Game(Base):
    name = db.Column(db.String(200), nullable=False)
    developer = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(1000), nullable=False)
    year = db.Column(db.Integer, nullable=False) 

    reviews = db.relationship("Review", backref="game", lazy=True)
    game_genres = db.relationship("GameGenre", backref="game", lazy=True)
    game_tags = db.relationship("GameTag", backref="game", lazy=True)

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


    def modify_tags(self, tag_ids): 
        GameTag.query.filter_by(game_id=self.id).delete()
        self.add_tags(tag_ids)

    def add_tags(self, tag_ids):
        def create_game_tag(tag_id):
            result = GameTag()
            result.game_id = self.id
            result.tag_id = tag_id
            return result

        game_tags = map(create_game_tag, tag_ids)
        db.session.add_all(game_tags)
        db.session.commit()


    #yhdistetty toiminnallisuutta, voisi heittää erilliseen utilities-luokkaankin
    @staticmethod
    def find_all_numbers_of_reviews_with_having_condition(condition="",param_name=None, param_value=None):
        query = "SELECT Game.id, COUNT(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.id "+ condition + ";"

        stmt = text(query)

        if param_value: 
            stmt = stmt.bindparams(
                bindparam(param_name, value=param_value, )
            )
       
        res = db.engine.execute(stmt)        
        return {row[0]:row[1] for row in res}


    @staticmethod
    def find_all_numbers_of_reviews(): 
        return Game.find_all_numbers_of_reviews_with_having_condition()

  

    @staticmethod
    def find_numbers_of_reviews_for_genre(genre_id):
        return Game.find_all_numbers_of_reviews_with_having_condition("HAVING Game.id IN (SELECT game_id FROM Game_genre WHERE genre_id = :genre_id)"
        ,"genre_id", genre_id)
 

    #samoin yhdistetty toiminnallisuutta
    @staticmethod
    def construct_review_averages_dictionary(res):
        review_averages = {}
        
        for row in res: 
            avg = row[1]
            # PostgreSQL:llä palautuskeskiarvojen tyyppi on decimal, jolla ei ole metodia is_integer()
            if os.environ.get("HEROKU"):
                avg = float(avg)

            if avg is None: 
                avg = ""
            elif avg.is_integer():
                avg = int(avg)
            else:
                avg = format(row[1], ".2f")
            review_averages[row[0]] = avg
            
        return review_averages     
    
    @staticmethod
    def find_all_averages_of_reviews():
        stmt = text("SELECT Game.id, AVG(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.id;")
        res = db.engine.execute(stmt)
        return Game.construct_review_averages_dictionary(res)

    @staticmethod
    def find_averages_of_reviews_for_genre(genre_id):

        stmt = text("SELECT Game.id, AVG(Review.points) FROM Game LEFT JOIN Review ON Game.id = Review.game_id GROUP BY Game.id"
        " HAVING Game.id IN (SELECT DISTINCT Game_genre.game_id FROM Game_genre WHERE Game_genre.genre_id = :genre_id);").params(genre_id=genre_id)
        res = db.engine.execute(stmt)
        return Game.construct_review_averages_dictionary(res)

    
    @staticmethod
    def find_all_unreviewed_games(user_id):
        stmt = text("SELECT DISTINCT Game.id, Game.name FROM Game"
                    " WHERE Game.id NOT IN (SELECT Game.id FROM Game JOIN Review ON Game.id = Review.game_id"
                    " WHERE Review.account_id = :user_id); "
                      ).params(user_id=user_id)

        res=db.engine.execute(stmt)
        return [{"id":row[0], "name":row[1]} for row in res]

        
        

