from application import db, bcrypt
from application.models import Base
from application.reviews.models import Review
from application.reactions.models import Reaction
from sqlalchemy.sql import text
from datetime import datetime, timedelta
from application import constants

class User(Base):

    __tablename__ = "account"
    
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    
    # db.String ei toimi PostgreSQL:ssä hashattuun salasanatoiminnallisuuteen
    # https://stackoverflow.com/questions/5881169/what-column-type-length-should-i-use-for-storing-a-bcrypt-hashed-password-in-a-d
    password_hash = db.Column(db.Binary(60), nullable = False)

    reviews = db.relationship("Review", backref="account", lazy=True)
    reactions = db.relationship("Reaction", backref="account", lazy=True)
    user_roles = db.relationship("UserRole", backref="account", lazy=True)
    
    def __init__(self, name, username, password): 
        self.name = name
        self.username = username
        self.password_hash = bcrypt.generate_password_hash(password)

    def password_matches(self, attempt):
        return bcrypt.check_password_hash(self.password_hash, attempt)

        
        
    def has_reviewed(self, game_id):
        return Review.query.filter_by(account_id=self.id, game_id=game_id).first() is not None
        
    def has_reacted(self, review_id):
        return Reaction.query.filter_by(account_id=self.id, review_id=review_id).first() is not None
    
    @staticmethod
    def find_users_with_no_reviews():
        stmt = text("SELECT Account.username FROM Account"
                    " WHERE Account.id NOT IN (SELECT DISTINCT Review.account_id FROM Review);")

        res = db.engine.execute(stmt)
        users = list(map(lambda row: {"username": row[0]}, res))
        return users
        
    def get_id(self):
        return self.id
    
    def is_active(self): 
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self): 
        return True

    def has_role(self, role_name):
        roles = self.roles()
        for role in roles:
            if role.name == role_name:
                return True
        return False

    def allowed_to_edit_review(self, review):
        if self.has_role("ADMIN"):
            return True
        if self.id != review.account_id:
            return False
        # ainakin paikallinen sqlite tallentaa ajat utc/gmt-aikavyöhykkeellä, joten käytetään samaa
        # - tässä kohtaa halutaan joka tapauksessa vain miettiä kuluneen ajan pituutta
        now = datetime.utcnow()
        too_late = review.date_created + timedelta(minutes=constants.EDITING_TIME_LIMIT)
        return now < too_late
    
    def roles(self):
        return Role.query.join(Role.user_roles).filter_by(account_id=self.id).all()




class Role(Base):
    name = db.Column(db.String(64), nullable=False)
    user_roles = db.relationship("UserRole", backref="role", lazy = True)


    def __init__(self, name):
        self.name = name
    

    # Käytetäänkö missään?
    @staticmethod
    def find_roles_for_user(user_id):
        stmt = text("SELECT DISTINCT Role.name FROM Role JOIN User_role"
                    " ON Role.id = User_role.role_id WHERE User_role.account_id = :user_id").params(user_id=user_id)

        res = db.engine.execute(stmt)
        roles = list(map(lambda row: row[0], res))
        return roles




class UserRole(Base):
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable = False)
