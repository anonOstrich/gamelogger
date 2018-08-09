from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField

class GameForm(FlaskForm): 
    name = StringField("Pelin nimi")
    developer = StringField("Kehittäjä")
    description = TextAreaField("Kuvaus")
    year = IntegerField("Julkaisuvuosi")
    
    class Meta: 
        csrf = False
