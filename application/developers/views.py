from application import app, db
from application.games.models import Game
from application.constants import GAME_RESULTS_PER_PAGE
from application.utilities import parse_to_int
from sqlalchemy import func, distinct
from flask import render_template, request


@app.route("/developers", methods=["GET"])
def developers_index():
    developers_info = Game.query.with_entities(Game.developer, func.count(Game.id)).group_by(Game.developer).all()

    return render_template("developers/list.html", developers_info = developers_info)


@app.route("/developers/<developer_name>", methods=["GET"])
@app.route("/developers/<developer_name>/page/<page_number>")
def developers_view(developer_name, page_number = 1, sort_column = 0, sort_direction = "ASC"): 
    columns = ["Game.id", "Game.name", "Game.developer", "Game.year", "COUNT(Review.points)", "AVG(Review.points)"]
    possible_sort_column  = request.args.get("sort_column")
    possible_sort_direction = request.args.get("sort_direction")
    
    if possible_sort_column: 
        sort_column = possible_sort_column
    if possible_sort_direction: 
        sort_direction = possible_sort_direction

    sort_column = parse_to_int(sort_column)
    page_number = parse_to_int(page_number)
    if not(page_number is not None and sort_column is not None and sort_direction in ["ASC", "DESC"]):
        return render_template("error.html", error = "Yrität antaa vääränlaisia parametreja")




    games_info = Game.find_all_info_sorted({"developer": developer_name}, page_number = page_number, 
    order_column = columns[sort_column], order_direction = sort_direction)

    base_url = "/developers/" + developer_name + "/page"
    return render_template("games/list.html", games_info = games_info, title = "Kehittäjä: " + developer_name, 
    page_number = page_number, last_page = len(games_info) < GAME_RESULTS_PER_PAGE, base_url = base_url)