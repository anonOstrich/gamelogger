from flask_wtf import FlaskForm
from sqlalchemy import inspect
from wtforms import SelectMultipleField, StringField, validators
from application.genres.models import Genre
from application import db
class GenreCreationForm(FlaskForm):
    name = StringField("Genren nimi:", [validators.Length(min = 1, max = 64, message = "Nimen pituus 1-64 merkkiä")])

    class Meta: 
        csrf = False

class GenreSelectionForm(FlaskForm):

    def genre_choices():
        # tarkistetaan että tietokantataulu genre on luotu. 
        # välttää virheen kun sovellus käynnistetään ilman olemassaolevaa tietokantaa
        insp = inspect(db.engine)
        if "genre" not in insp.get_table_names():
            return []
        
        genres = Genre.query.all()
        genre_list = []
        for g in genres: 
            genre_list.append((g.id, g.name))
        return genre_list
        

    genre_ids = SelectMultipleField("Valitse genret",  choices = genre_choices(), coerce = int)

    class Meta:
        csrf = False