from application.forms import BaseForm, length_validators, MultiCheckboxField
from wtforms import IntegerField, StringField, DecimalField, validators
from application.genres.models import Genre

class SearchForm(BaseForm):
    name = StringField("Nimi", length_validators(max=200, optional=True))
    min_year = IntegerField("Vuosi(min)", [validators.Optional()]) 
    max_year = IntegerField("Vuosi(max)", [validators.Optional()])
    developer = StringField("Kehittäjä", length_validators(max=100, optional=True))
    genres = MultiCheckboxField("Genret", [validators.Optional()], coerce=int)
    tags = MultiCheckboxField("Omat tägit", [validators.Optional()], coerce=int)
    min_average = DecimalField("Arvostelujen keskiarvo(min)", [validators.Optional()])
    max_average = DecimalField("Arvostelujen keskiarvo(max)", [validators.Optional()])
    min_count = IntegerField("Arvostelujen lukumäärä(min)", [validators.Optional()])
    max_count = IntegerField("Arvostelujen lukumäärä(max)", [validators.Optional()])


    def __init__(self, *args, **kwargs):
        super(SearchForm, self).__init__(*args, **kwargs)
        self.genres.choices =  [(g.id, g.name) for g in Genre.query.all()]
    

    def set_tags_info(self, user):
        self.tags.choices = [(t.id, t.name) for t in user.tags()]

    