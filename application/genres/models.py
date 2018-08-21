from application import db
from application.models import Base

class Genre(Base):
    name = db.Column(db.String(128), nullable = False, unique = True)

    game_genres = db.relationship("GameGenre", backref="genre", lazy = True)
    
    def __init__(self, name):
        self.name = name


class GameGenre(Base):
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable = False)
    genre_id = db.Column(db.Integer, db.ForeignKey("genre.id"), nullable = False)