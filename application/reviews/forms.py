from flask_wtf import FlaskForm
from wtforms import TextAreaField, IntegerField, validators

class ReviewForm(FlaskForm):
    text = TextAreaField("Arvostelu", [validators.Length(min=2, max=2000)])
    points = IntegerField("Arvosana (1-10)", [validators.NumberRange(min=1, max=10)])
    
    class Meta: 
        csrf = False
