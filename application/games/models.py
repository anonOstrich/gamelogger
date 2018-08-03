from application import db

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime, default=db.func.current_timestamp(),
    onupdate=db.func.current_timestamp())

    name = db.Column(db.String(255), nullable=False)
    developer = db.Column(db.String(255), nullable=False)
    year = db.Column(db.Integer, nullable=False) 
    completed=db.Column(db.Boolean, nullable=False)


    def __init__(self, name, developer, year):
        self.name = name
        self.developer = developer
        self.year = year
        self.completed = False

