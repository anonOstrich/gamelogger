from application.forms import BaseForm, MultiCheckboxField, length_validators
from sqlalchemy import inspect
from wtforms import StringField, validators
from application.genres.models import Genre


class GenreCreationForm(BaseForm):
    name = StringField("Genren nimi:", length_validators(max=64))



class GenreSelectionForm(BaseForm):
    genre_ids = MultiCheckboxField("Valitse genret", coerce = int)

    def __init__(self, *args, **kwargs):
        super(GenreSelectionForm, self).__init__(*args, **kwargs)
        self.genre_ids.choices = [(genre.id, genre.name) for genre in Genre.query.all()]
