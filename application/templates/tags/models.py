from application import db 
from application.models import Base

class Tag(Base):
    name = db.Column(db.String(200), nullable = False)
    account_id = db.Column(db.Integer(), db.ForeigKey("account.id"), nullable = False)

    game_tags = db.relationship("GameTag", backref="tag", lazy = True)

    def __init__(self, name):
        self.name = name


class GameTag(Base):
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable = False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable = False)