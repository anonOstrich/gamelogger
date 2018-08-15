from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, TextAreaField, validators

class GameForm(FlaskForm): 
    name = StringField("Pelin nimi", [validators.Length(max=200, message="Liian pitkä nimi (korkeintaan 200 merkkiä)"), validators.Length(min=1, message="Syötä nimi")])
    developer = StringField("Kehittäjä", [validators.Length(min=1, max=100, message="Oltava 1-100 merkin pituinen")])
    description = TextAreaField("Kuvaus (korkeintaan 1000 merkkiä)", [validators.Length(min=1, max=1000, message="Kuvauksen oltava 1-1000 merkkiä pitkä")])
    year = IntegerField("Julkaisuvuosi", [validators.NumberRange(min=0, max=2020, message="Oltava kokonaisluku väliltä 0-2020")])
    
    class Meta: 
        csrf = False
