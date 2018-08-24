from flask import Flask
app = Flask(__name__)

# turvallisuustoiminnallisuus
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)
app.config["BCRYPT_HANDLE_LONG_PASSWORDS"] = True


# tietokanta ja ORM
from flask_sqlalchemy import SQLAlchemy 
import os

if os.environ.get("HEROKU"):
    app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL")
else: 
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///games.db"
    app.config["SQLALCHEMY_ECHO"] = True


db = SQLAlchemy(app)


# kirjautumistoiminnallisuus
from os import urandom
app.config["SECRET_KEY"] = urandom(32)

from flask_login import LoginManager, current_user
login_manager = LoginManager()
login_manager.setup_app(app)

login_manager.login_view = "auth_login"
login_manager.login_message = "Kirjaudu sisään käyttääksesi toimintoa"

# roolitoiminnallisuus
from functools import wraps
from application.auth.models import Role

def login_required(role="ANY"):    
    def wrapper(fn):
        @wraps(fn)
        def decorated_view(*args, **kwargs):
            if not current_user.is_authenticated:
                return login_manager.unauthorized()
            
            unauthorized = False

            if role != "ANY":
                unauthorized = True
            
            for user_role in Role.find_roles_for_user(current_user.id):
                if user_role == role:
                    unauthorized = False
                    break
            
            if unauthorized: 
                return login_manager.unauthorized()
            
            return fn(*args, **kwargs)
        return decorated_view
    return wrapper


# ladataan sovelluksen toiminnallisuus
from application import views

from application.games import models
from application.games import views

from application.auth import models
from application.auth import views

from application.reviews import models
from application.reviews import views

from application.reactions import models
from application.reactions import views

from application.genres import models
from application.genres import views

from application.auth.models import User, UserRole

# kirjautumistoiminnallisuutta lisää

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


# tietokannan luonti
try: 
    db.create_all()
    # Alustetaan tietokanta jos sitä ei ole vielä luotu 
    salt = "RANDOM"
    admin = User("Admin Hallitsija", "admin","admin_salasana")
    admin_role = Role("ADMIN") 
    normal = User("Esimerkki Käyttäjä", "testi", "salasana")
    default_role = Role("DEFAULT") 
    db.session.add_all((admin, normal, admin_role, default_role))
    db.session.commit()
    # vasta nyt pääavaimet on luotu

    #TODO:
    # Voisi ehkä toteuttaa liittämisen muualla? Esim user.addRole(Role)
    # Pitää ehkä silti muistaa ensin committaa, jotaa pääavaimet luodaan...? 
    ur1 = UserRole() 
    ur1.account_id = admin.id
    ur1.role_id = admin_role.id
    ur2 = UsertRole()
    ur2.account_id = normal.id 
    ur2.role_id = default_role.id

    db.session.add_all((ur1, ur2))
    db.session.commit()
except: 
    pass
