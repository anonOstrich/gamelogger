from application.forms import BaseForm, length_validators
from wtforms import StringField, IntegerField, TextAreaField, validators
from application.constants import LAST_ACCEPTABLE_RELEASE_YEAR


class GameForm(BaseForm): 
    name = StringField("Pelin nimi", length_validators(max=200))
    developer = StringField("Kehittäjä", length_validators(max=100))
    description = TextAreaField("Kuvaus (korkeintaan 1000 merkkiä)", length_validators(max=1000))
    year = IntegerField("Julkaisuvuosi",
     [validators.NumberRange(min=0, max=LAST_ACCEPTABLE_RELEASE_YEAR, message=str("Oltava kokonaisluku väliltä 0-" + str(LAST_ACCEPTABLE_RELEASE_YEAR)))])