from flask import render_template
from application import app
from application.games.models import Game
from application.auth.models import User
from flask_login import current_user, login_required


@app.route("/")
def index():
    unreviewed_games = []
    if current_user.is_authenticated:
        unreviewed_games = Game.find_all_unreviewed_games(current_user.id)

    top_games = Game.find_top_five_games()
    general_details = Game.find_general_details()
    
    return render_template("index.html", unreviewed_games = unreviewed_games, general_details = general_details,  top_games = top_games)
    


