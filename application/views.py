from flask import render_template
from application import app 
from application.games.models import Game
from application.auth.models import User
from flask_login import current_user


@app.route("/")
def index():
    unreviewed_games = []
    if current_user.is_authenticated:
        unreviewed_games = Game.find_unreviewed_games(current_user.id)
    
    return render_template("index.html", unreviewed_games = unreviewed_games, users = User.find_users_with_no_reviews())
    
