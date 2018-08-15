from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, validators

class ReviewForm(FlaskForm):
    text = TextAreaField("Arvostelu", [validators.Length(min=2, max=2000, message="Arvion oltava 2-2000 merkkiä pitkä")])
    points = IntegerField("Arvosana (1-10)", [validators.NumberRange(min=1, max=10, message="Arvosanan oltava väliltä 1-10")])
    
    class Meta: 
        csrf = False
