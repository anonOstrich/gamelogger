from application import db, bcrypt
from application.models import Base
from application.reviews.models import Review
from application.reactions.models import Reaction
from application.tags.models import Tag
from sqlalchemy.sql import text
from sqlalchemy.schema import UniqueConstraint
from datetime import datetime, timedelta
from application import constants


class Role(Base):
    name = db.Column(db.String(64), nullable=False)


    user_roles = db.relationship("UserRole", backref="role", lazy = True)

    def __init__(self, name):
        self.name = name


class User(Base):

    __tablename__ = "account"
    
    name = db.Column(db.String(100), nullable=False)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password_hash = db.Column(db.Binary(60), nullable = False)
    description = db.Column(db.String(1000))

    reviews = db.relationship("Review", backref="account", lazy=True)
    reactions = db.relationship("Reaction", backref="account", lazy=True)
    user_roles = db.relationship("UserRole", backref="account", lazy=True)
    
    def __init__(self, name, username, password, description): 
        self.name = name
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password)
        self.description = description

    def password_matches(self, attempt):
        return bcrypt.check_password_hash(self.password_hash, attempt)

    # flask-loginin vaatimat metodit
    def get_id(self):
        return self.id
    
    def is_active(self): 
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self): 
        return True


    # roolien tarkasteluun ja lisäämiseen liittyvät metodit
    def roles(self):
        return Role.query.join(Role.user_roles).filter_by(account_id=self.id).all()

    def has_role(self, role_name):
        roles = self.roles()
        for role in roles:
            if role.name == role_name:
                return True
        return False


    # parametreina rooliolioita
    def add_roles(self, *args):
        def create_user_role(r):
            result = UserRole()
            result.account_id = self.id 
            result.role_id = r.id 
            return result
        
        user_roles = map(create_user_role, args)
        db.session.add_all(user_roles)
        db.session.commit()


    def add_role(self, role):
        self.add_roles(role)
    
    # tagitoiminnallisuutta
    def tags(self):
        return Tag.query.filter_by(account_id = self.id).all()
        
    # metodit joilla selvitetään käyttäjän toimintaa sovelluksessa     
    #        
    def has_reviewed(self, game):
        return Review.query.filter_by(account_id=self.id, game_id=game.id).first() is not None
        
    def has_reacted_to(self, review):
        return Reaction.query.filter_by(account_id=self.id, review_id=review.id).first() is not None
        

    def is_allowed_to_edit_review(self, review):
        if self.has_role("ADMIN"):
            return True
        if self.id != review.account_id:
            return False
        # ainakin paikallinen sqlite tallentaa ajat utc/gmt-aikavyöhykkeellä, joten käytetään samaa
        # tässä kohtaa halutaan joka tapauksessa vain miettiä kuluneen ajan pituutta
        now = datetime.utcnow()
        too_late = review.date_created + timedelta(minutes=constants.EDITING_TIME_LIMIT)
        return now < too_late

    

    @staticmethod
    def find_users_with_no_reviews():
        stmt = text("SELECT Account.username FROM Account"
                    " WHERE Account.id NOT IN (SELECT DISTINCT Review.account_id FROM Review);")

        res = db.engine.execute(stmt)
        users = list(map(lambda row: {"username": row[0]}, res))
        return users

    @staticmethod 
    def user_exists_with_username(username):
        return User.query.filter_by(username=username).first() is not None    


class UserRole(Base):
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable = False)

    unique_role = UniqueConstraint(account_id, role_id)
