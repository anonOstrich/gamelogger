from application.forms import BaseForm, length_validators
from wtforms import StringField, IntegerField, TextAreaField, validators
from datetime import date

next_year = date.today().year + 1

class GameForm(BaseForm): 
    name = StringField("Pelin nimi", length_validators(max=200))
    developer = StringField("Kehittäjä", length_validators(max=100))
    description = TextAreaField("Kuvaus (korkeintaan 1000 merkkiä)", length_validators(max=1000))
    year = IntegerField("Julkaisuvuosi",
     [validators.NumberRange(min=0, max=next_year, message=str("Oltava kokonaisluku väliltä 0-" + str(next_year)))])