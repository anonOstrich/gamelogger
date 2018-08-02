from application import db

class Movie(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    date_created=db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified=db.Column(db.DateTime, default=db.func.current_timestamp(), onupdate=db.func.current_timestamp())
    
    name=db.Column(db.String(255), nullable=False)
    runtime=db.Column(db.Integer, nullable=False) # Tarkistuksia, esim yli 0? Tehdäänkö tässä tiedostossa?
    director=db.Column(db.String(255), nullable=False)
    year=db.Column(db.Integer, nullable=False)
    
    
    # To be considered: synopsis, genre, tags, related reviews...
    
    def __init__(self, name, director, year, runtime):
        self.name = name
        self.director = director
        self.year = year
        self.runtime = runtime
        
                       
    
    
