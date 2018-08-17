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
        


    # Haetaan täsmälleen tarpeellinen määrä tietoa tietokannasta yhdellä kertaa
    # positiivisella reaktiolla positive = 1, negatiivisella positive = 0. 
    # yhden arvion reaktiojen lkm(positive) = lkm(positiiviset) + lkm(negatiiviset).
    # koska sum(positive) = lkm(positive), lkm(negatiiviset) = lkm(positive) - sum(positive)
    @staticmethod
    def find_all_reactions_for_reviews_of_game(game_id):
        stmt = text("SELECT Review.id, SUM(Reaction.positive), COUNT(Reaction.positive)"
                    " FROM Review LEFT JOIN Reaction ON Review.id = Reaction.review_id"
                    " WHERE Review.game_id = :game_id GROUP BY Review.id"
                    " HAVING COUNT(Reaction.positive) > 0;").params(game_id=game_id)
        res = db.engine.execute(stmt)

        result = {}

        for row in res: 
            rev_id = row[0]
            num_positives = row[1]
            num_negatives = row[2] - num_positives
            result[rev_id] = (num_positives, num_negatives)
            print("*********************************")
            print(result[rev_id])
        
        return result

