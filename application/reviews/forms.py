from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, validators

class ReviewForm(FlaskForm):

    def points_choices():
        result=[]
        for i in range(1, 11):
            result.append((i, i))
        return result    
    
    text = TextAreaField("Arvostelu", [validators.Length(min=2, max=2000, message="Arvion oltava 2-2000 merkkiä pitkä")])
    points = RadioField("Arvosana", [validators.InputRequired(message="Valitse arvosana")], 
                        choices=points_choices(), coerce=int)
    
    
    class Meta: 
        csrf = False
        
