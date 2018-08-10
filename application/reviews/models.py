from application import db

class Review(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created=db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified=db.Column(db.DateTime, default=db.func.current_timestamp())
    
    text = db.Column(db.String(2000), nullable=False)
    points = db.Column(db.Integer, nullable=False)
    
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey("game.id"), nullable=False)
    
    def __init__(self, text, points):
        self.text = text
        self.points = points
    
    
