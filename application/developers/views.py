from application import app, db
from application.games.models import Game
from application.constants import GAME_RESULTS_PER_PAGE
from sqlalchemy import func, distinct
from flask import render_template


@app.route("/developers", methods=["GET"])
def developers_index():
    developers_info = Game.query.with_entities(Game.developer, func.count(Game.id)).group_by(Game.developer).all()

    return render_template("developers/list.html", developers_info = developers_info)


@app.route("/developers/<developer_name>", methods=["GET"])
@app.route("/developers/<developer_name>/pages/<page_number>")
def developers_view(developer_name, page_number = 1): 

    games_info = Game.find_all_info({"developer": developer_name}, page_number = int(page_number))
    base_url = "/developers/" + developer_name
    return render_template("games/list.html", games_info = games_info, title = "Kehittäjä: " + developer_name, 
    page_number = int(page_number), last_page = len(games_info) < GAME_RESULTS_PER_PAGE, base_url = base_url)