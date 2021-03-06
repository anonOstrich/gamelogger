from application.forms import BaseForm, length_validators
from wtforms import StringField, PasswordField, TextAreaField, validators

class LoginForm(BaseForm): 
    username = StringField("Käyttäjätunnus",  length_validators(max=100))
    password = PasswordField("Salasana", length_validators(6, 32))


class RegisterForm(BaseForm): 
    name = StringField("Nimi", length_validators(max=100))
    username = StringField("Käyttäjätunnus", length_validators(max=100))
    password = PasswordField("Salasana (vähintään 6 merkkiä)",
     length_validators(6, 32) + [validators.InputRequired(), 
     validators.EqualTo("password_confirm", message = "Salasanat eivät täsmää")])
    password_confirm = PasswordField("Toista salasana", length_validators(6, 32))
    description = TextAreaField("Lyhyt kuvaus itsestäsi (vapaaehtoinen)", length_validators(max=1000, optional=True))

class DescriptionForm(BaseForm):
    description = TextAreaField("", length_validators(max=1000))
