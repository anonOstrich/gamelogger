from application import db
from application.models import Base
from sqlalchemy.sql import text
from sqlalchemy.schema import UniqueConstraint

class Genre(Base):
    name = db.Column(db.String(128), nullable = False, unique = True)

    game_genres = db.relationship("GameGenre", backref="genre", lazy = True)
    
    def __init__(self, name):
        self.name = name

    @staticmethod
    def find_genres_sorted_by_number_of_games():
        stmt = text("SELECT Genre.id, Genre.name, COUNT(Game_genre.game_id)"
                    " FROM Genre LEFT JOIN Game_genre ON Genre.id = Game_genre.genre_id"
                    " GROUP BY Genre.id ORDER BY COUNT(Game_genre.game_id) DESC;")
        res = db.engine.execute(stmt)
        sorted_list = []
        for row in res: 
            sorted_list.append({"id": row[0], "name": row[1], "number_of_games": row[2]})

        return sorted_list


class GameGenre(Base):
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable = False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable = False)

    unique_rule = UniqueConstraint(game_id, genre_id)