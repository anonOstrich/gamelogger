from flask_wtf import FlaskForm
from wtforms import StringField, validators

class GenreForm(FlaskForm):
    name = StringField("Genren nimi:", [validators.Length(min = 1, max = 64, message = "Nimen pituus 1-64 merkkiä")])

    class Meta: 
        csrf = False