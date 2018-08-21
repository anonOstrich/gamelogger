from application import db 
from application.models import Base
from application.reviews.models import Review
from application.reactions.models import Reaction
from sqlalchemy.sql import text

import traceback

class User(Base):

    __tablename__ = "account"
    
    name = db.Column(db.String(144), nullable=False)
    username = db.Column(db.String(144), nullable=False, unique=True)
    password = db.Column(db.String(144), nullable=False)
    
    reviews = db.relationship("Review", backref="account", lazy=True)
    reactions = db.relationship("Reaction", backref="account", lazy=True)
    userroles = db.relationship("UserRole", backref="account", lazy=True)
    
    def __init__(self, name, username, password): 
        self.name = name
        self.username = username
        self.password = password
        
        
    def has_reviewed(self, game_id):
        return Review.query.filter_by(account_id=self.id, game_id=game_id).first() is not None
        
    def has_reacted(self, review_id):
        return Reaction.query.filter_by(account_id=self.id, review_id=review_id).first() is not None
    
    @staticmethod
    def find_users_with_no_reviews():
        stmt = text("SELECT Account.username FROM Account"
                    " WHERE Account.id NOT IN (SELECT DISTINCT Review.account_id FROM Review);")

        res = db.engine.execute(stmt)
        users=[]
        for row in res:
            users.append({"username": row[0]})
        return users
        
    def get_id(self):
        return self.id
    
    def is_active(self): 
        return True
    
    def is_anonymous(self):
        return False
    
    def is_authenticated(self): 
        return True


class Role(Base):
    name = db.Column(db.String(64), nullable=False)
    userRoles = db.relationship("UserRole", backref="role", lazy = True)


    def __init__(self, name):
        self.name = name
    
    @staticmethod
    def find_roles_for_user(user_id):
        stmt = text("SELECT DISTINCT Role.name FROM Role JOIN User_role"
                    " ON Role.id = User_role.role_id WHERE User_role.account_id = :user_id").params(user_id=user_id)

        res = db.engine.execute(stmt)
        roles = []
        for row in res: 
            roles.append(row[0])
        return roles


class UserRole(Base):
    account_id = db.Column(db.Integer, db.ForeignKey("account.id"), nullable = False)
    role_id = db.Column(db.Integer, db.ForeignKey("role.id"), nullable = False)
