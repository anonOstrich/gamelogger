from application import db
from application.models import Base
from sqlalchemy.schema import UniqueConstraint

class Reaction(Base): 
    positive = db.Column(db.Boolean, nullable=False)
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    review_id = db.Column(db.Integer, db.ForeignKey("review.id"), nullable=False)
    
    one_reaction_rule = UniqueConstraint(account_id, review_id)
    
    def __init__(self, positive):
        self.positive = positive
        
