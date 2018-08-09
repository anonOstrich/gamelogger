from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class LoginForm(FlaskForm): 
    username = StringField("Käyttäjätunnus",  [validators.Length(min=1)])
    password = PasswordField("Salasana")    
    
    class Meta: 
        csrf = False
    

class RegisterForm(FlaskForm): 
    name = StringField("Nimi", [validators.Length(min=2)])
    username = StringField("Käyttäjätunnus", [validators.Length(min=1)])
    password = PasswordField("Salasana (vähintään 6 merkkiä)", [validators.Length(min=6)])
    
    class Meta: 
        csrf = False
