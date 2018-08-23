from flask_wtf import FlaskForm
from wtforms import SelectMultipleField, widgets, ValidationError


class BaseForm(FlaskForm):

    class Meta:
        csrf = False


# kuten toteutettu https://gist.github.com/doobeh/4668212
class MultiCheckboxField(SelectMultipleField):
    widget = widgets.ListWidget(prefix_label=False)
    option_widget = widgets.CheckboxInput()


def min_length(min):
    message = "Vähintään " + str(min) + " merkkiä pitkä"

    def _min_length(form, field):
        input = field.data
        if len(input) < min:
            raise ValidationError(message) 

    return _min_length


def max_length(max):
    message = "Korkeintaan " + str(max) + " merkkiä pitkä"
    
    def _max_length(form, field):
        input = field.data
        if len(input) > max:
            raise ValidationError(message)

    return _max_length



def length_validators(min=1, max = -1):
    if max < 0: 
        raise ValueError("Ylärajaa ei asetettu")
    return [min_length(min), max_length(max)]