from application.forms import BaseForm, length_validators
from wtforms import TextAreaField, RadioField, validators

class ReviewForm(BaseForm):

    text = TextAreaField("Arvostelu", length_validators(max=1000))
    points = RadioField("Arvosana", [validators.InputRequired(message="Valitse arvosana")], 
                       choices=list(map(lambda i: (i,i), range(1,11))),  coerce=int)
        
