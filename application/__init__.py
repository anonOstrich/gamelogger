#flask
from flask import Flask
app = Flask(__name__)

#tietokanta
from flask_sqlalchemy import SQLAlchemy 
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else: 
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.db"
    app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)

#oma sovellus
from application import views

from application.games import models
from application.games import views

from application.auth import models
from application.auth import views

from application.reviews import models
from application.reviews import views

from application.reactions import models
from application.reactions import views

#kirjautuminen
from application.auth.models import User, Role, UserRole
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager
login_manager = LoginManager()
login_manager.init_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Rekisteröidy tai kirjaudu sisään käyttääksesi toimintoa"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


try: 
    db.create_all()
    # Alustetaan tietokanta jos sitä ei ole vielä luotu 
    u = User("Urho Sydänkarhu", "otso", "mesikammen")
    admin_role = Role("ADMIN") 
    default_role = Role("DEFAULT") 
    db.session.add_all((u, admin_role, default_role))
    db.session.commit()
    # vasta nyt pääavaimet on luotu
    ur = UserRole() 
    ur.account_id = u.id
    ur.role_id = admin_role.id
    #luodaan oletusrooli valmiiksi tietokantaan
    db.session.add(ur)
    db.session.commit()
except: 
    pass
