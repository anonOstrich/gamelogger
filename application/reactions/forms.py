from flask_wtf import FlaskForm
from wtforms import RadioField, HiddenField

class ReactionForm(FlaskForm): 
    positivity = RadioField("Tykkään arvostelusta", choices=[(1, "Tykkään"), (0, "En tykkää")], coerce=int)
    
    class Meta:
        csrf = False
        

