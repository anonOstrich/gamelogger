from application import db 
from application.models import Base
from sqlalchemy.sql import text
from sqlalchemy.schema import UniqueConstraint

class Tag(Base):
    name = db.Column(db.String(200), nullable = False)
    account_id = db.Column(db.Integer(), db.ForeignKey("account.id"), nullable = False)

    game_tags = db.relationship("GameTag", backref="tag", lazy = True)

    one_name_rule = UniqueConstraint(name, account_id)

    def __init__(self, name):
        self.name = name

    # aakkosjärjestyksessä, mutta myöhemmin ehkä halutaan muitakin vaihtoehtoja
    @staticmethod
    def find_all_tags_and_numbers_of_tagged_games(user_id): 
        stmt = text("SELECT Tag.id, Tag.name, COUNT(Game_tag.id) FROM Tag LEFT JOIN Game_tag"
        " ON Tag.id = Game_tag.tag_id WHERE Tag.account_id = :user_id"
        " GROUP BY Tag.id ORDER BY Tag.name ASC;"
        ).params(user_id=user_id)

        res = db.engine.execute(stmt)
        return [{"id":row[0], "name":row[1], "number_of_games":row[2]} for row in res]


class GameTag(Base):
    tag_id = db.Column(db.Integer, db.ForeignKey("tag.id"), nullable = False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable = False)

    # Samaa (saman käyttäjän samannimistä) tagia ei voi lisätä pelille kahdesti
    one_game_tag_rule = UniqueConstraint(tag_id, game_id)