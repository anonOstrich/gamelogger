from application.forms import BaseForm, length_validators, MultiCheckboxField
from wtforms import IntegerField, StringField

class SearchForm(BaseForm):
    name = StringField()
    minYear = IntegerField() 
    maxYear = IntegerField()
    developer = StringField()
    genres = MultiCheckboxField()
    tags = MultiCheckboxField()

    