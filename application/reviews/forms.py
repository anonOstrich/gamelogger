from flask_wtf import FlaskForm
from wtforms import TextAreaField, RadioField, validators

class ReviewForm(FlaskForm):
    text = TextAreaField("Arvostelu", [validators.Length(min=2, max=2000, message="Arvion oltava 2-2000 merkkiä pitkä")])
    points = RadioField("Arvosana", [validators.InputRequired(message="Valitse arvosana")], 
                        choices=[(1,1), (2,2), (3,3), (4,4), (5,5), (6,6), (7,7), (8,8), (9,9), (10,10)], coerce=int)
    
    # Saisiko myöhemmin toimimaan?
    #def points_choices():
        #result=[]
        #for i in range(1, 10):
            #result.append((i, i))
        #return result        
        
    
    class Meta: 
        csrf = False
        
