from application import db
from application.models import Base

class Review(Base):
    
    text = db.Column(db.String(2000), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    
    def __init__(self, text, points):
        self.text = text
        self.points = points
    
    
