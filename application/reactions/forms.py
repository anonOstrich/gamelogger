from flask_wtf import FlaskForm
from wtforms import RadioField

class ReactionForm(FlaskForm): 
    positivity = RadioField("Tykkään arvostelusta", choices=[("positive", "Tykkään"), ("negative", "En tykkää")])
    
    class Meta:
        csrf = False
