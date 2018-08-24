from application import db
from application.models import Base
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy.sql import text

class Reaction(Base): 
    positive = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    
    one_reaction_rule = UniqueConstraint(account_id, review_id)
    
    def __init__(self, positive):
        self.positive = positive

    @staticmethod
    def delete_reactions_relating_to_game(game_id):
        stmt = text("DELETE FROM Reaction WHERE review_id IN"
                    " (SELECT id FROM Review WHERE game_id=:game_id);").params(game_id=game_id)
        res = db.engine.execute(stmt)
        res.close()

        


    # Haetaan täsmälleen tarpeellinen määrä tietoa tietokannasta yhdellä kertaa
    # positiivisella reaktiolla positive = 1, negatiivisella positive = 0. 
    # yhden arvion reaktiojen lkm(positive) = lkm(positiiviset) + lkm(negatiiviset).
    # koska sum(positive) = lkm(positive), lkm(negatiiviset) = lkm(positive) - sum(positive)
    @staticmethod
    def find_all_reactions_for_reviews_of_game(game_id):
        stmt = text("SELECT Review.id, SUM(CASE WHEN Reaction.positive THEN 1 ELSE 0 END), COUNT(Reaction.positive)"
                    " FROM Review LEFT JOIN Reaction ON Review.id = Reaction.review_id"
                    " WHERE Review.game_id = :game_id GROUP BY Review.id HAVING COUNT(Reaction.positive) > 0").params(game_id=game_id)
        res = db.engine.execute(stmt)


        result = {}
        
        for row in res: 
            rev_id = row[0]
            num_positives = row[1]
            num_negatives = row[2] - num_positives

            percentage_positives = int(100*(float(num_positives) / (num_negatives + num_positives)))
            result[rev_id] = (num_positives, num_negatives, percentage_positives)

        
        return result

