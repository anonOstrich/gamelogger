from flask_wtf import FlaskForm
from sqlalchemy import inspect
from wtforms import SelectMultipleField, StringField, validators, widgets
from application.genres.models import Genre
from application import db



class GenreCreationForm(FlaskForm):
    name = StringField("Genren nimi:", [validators.Length(min = 1, max = 64, message = "Nimen pituus 1-64 merkkiä")])

    class Meta: 
        csrf = False


# kuten toteutettu https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


# Genrelista ei taida aina päivittyä.... 
class GenreSelectionForm(FlaskForm):
    genre_ids = MultiCheckboxField("Valitse genret", coerce = int)

    def __init__(self, *args, **kwargs):
        super(GenreSelectionForm, self).__init__(*args, **kwargs)
        self.genre_ids.choices = [(genre.id, genre.name) for genre in Genre.query.all()]

    class Meta:
        csrf = False