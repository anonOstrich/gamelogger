from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, validators

class GameForm(FlaskForm): 
    name = StringField("Pelin nimi", [validators.Length(min=2)])
    developer = StringField("Kehittäjä", [validators.Length(min=2)])
    description = TextAreaField("Kuvaus", [validators.Length(min=2, max=500)])
    #max = nykyinen vuosi? hieman yli nykyinen vuosi? 
    year = IntegerField("Julkaisuvuosi", [validators.NumberRange(min=1900, max=2018)])
    
    class Meta: 
        csrf = False
