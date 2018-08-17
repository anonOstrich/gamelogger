from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, validators

class LoginForm(FlaskForm): 
    username = StringField("Käyttäjätunnus",  [validators.Length(min=1, max=32, message="Tunnuksen pituuden oltava 1-32")])
    password = PasswordField("Salasana", [validators.InputRequired(message="Ei voi olla tyhjä"), validators.Length(max=32, message="Liian pitkä salasana")])    
    
    class Meta: 
        csrf = False
    

class RegisterForm(FlaskForm): 
    name = StringField("Nimi", [validators.Length(min=1, max=100, message="Nimen pituus 1-100 merkkiä")])
    username = StringField("Käyttäjätunnus", [validators.Length(min=1, max=32, message="Valitse tunnus, jonka pituus on 1-32 merkkiä")])
    password = PasswordField("Salasana (vähintään 6 merkkiä)", [validators.Length(min=6, max=32, message="Salasanan oltava 6-32 merkkiä pitkä")])
    
    class Meta: 
        csrf = False
