from application.forms import BaseForm, length_validators
from wtforms import StringField, PasswordField, validators

class LoginForm(BaseForm): 
    username = StringField("Käyttäjätunnus",  length_validators(max=100))
    password = PasswordField("Salasana", length_validators(6, 32))


class RegisterForm(BaseForm): 
    name = StringField("Nimi", length_validators(max=100))
    username = StringField("Käyttäjätunnus", length_validators(max=100))
    password = PasswordField("Salasana (vähintään 6 merkkiä)", length_validators(6, 32))
