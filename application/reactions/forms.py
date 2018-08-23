from application.forms import BaseForm
from wtforms import RadioField, HiddenField

class ReactionForm(BaseForm): 
    positivity = RadioField("Tykkään arvostelusta", choices=[(1, "Tykkään"), (0, "En tykkää")], coerce=int)
        

