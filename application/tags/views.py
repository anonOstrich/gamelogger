from flask import render_template, redirect, request, url_for
from flask_login import current_user  

from application import app, db, login_required
from application.auth.models import User
from application.tags.models import Tag, GameTag
from application.games.models import Game
from application.tags.forms import TagCreationForm, TagSelectionForm

from application.constants import GAME_RESULTS_PER_PAGE
from application.utilities import parse_to_int

@app.route("/tags/<user_id>/", methods=["GET"])
def tags_index(user_id): 
    tag_owner = User.query.get(user_id)
    tags_info = Tag.find_all_tags_and_numbers_of_tagged_games(user_id)
    return render_template("tags/list.html", tag_owner=tag_owner, tags_info = tags_info, form = TagCreationForm())


@app.route("/tags/<user_id>", methods=["POST"])
@login_required()
def tags_create(user_id):
    user = User.query.get(user_id)

    if not user: 
        return render_template("error.html", error ="Käyttäjää ei  ole olemassa")
    if current_user.id != user.id and  not current_user.has_role("ADMIN"): 
        return render_template("error.html", error ="Sinulla ei ole oikeuksia lisätä tägejä toiselle käyttäjälle")  

    form = TagCreationForm(request.form)
    if not form.validate():
        tags_info = Tag.find_all_tags_and_numbers_of_tagged_games(user_id)
        return render_template("tags/list.html", tag_owner=user, tags_info = tags_info, form = form)



    tag = Tag(form.name.data)
    tag.account_id = user_id
    db.session.add(tag)
    db.session.commit()
    return redirect(url_for("tags_index", user_id=user_id))



@app.route("/tags/modify/<game_id>", methods=["GET", "POST"])
@login_required()
def tags_modify(game_id):
    game = Game.query.get(game_id)
    if not game: 
        return render_template("error.html", error = "Peliä ei ole tietokannassa")

    if request.method == "GET":
        form = TagSelectionForm()
        form.set_choices_for_user(current_user)
        form.select_users_tags_for_game(current_user, game)
        return render_template("tags/link.html", form = form, game = game)

    form = TagSelectionForm(request.form)
    game.modify_tags(form.tag_ids.data)
    return redirect(url_for("games_view", game_id=game_id))


@app.route("/tags/<tag_id>/delete", methods=["POST"])
@login_required()
def tags_delete(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag: 
        return render_template("error.html", error = "Tagia ei ole olemassa")
    owner_id = tag.account_id
    if owner_id != current_user.id and  not current_user.has_role("ADMIN"):
        return render_template("error.html", error = "Et voi poistaa toisen tagia")

    
    GameTag.query.filter(GameTag.tag_id==tag_id).delete()
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for("tags_index", user_id=owner_id))



@app.route("/tags/<tag_id>/games", methods=["GET"])
@app.route("/tags/<tag_id>/games/page/<page_number>", methods=["GET"])
def tag_games(tag_id, page_number = 1, sort_column = 0, sort_direction="ASC"): 

    tag = Tag.query.filter(Tag.id == tag_id).first()

    if not tag: 
        return render_template("error.html",  error = "Tagia ei ole olemassa")

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



    games_info = Game.find_all_info_sorted({"tags": [int(tag_id)]}, page_number = page_number,
        order_column = columns[sort_column], order_direction = sort_direction
    )

    base_url = "/tags/" + tag_id + "/games/page"

    return render_template("games/list.html", games_info = games_info, base_url = base_url, page_number = page_number, 
    last_page = len(games_info) < GAME_RESULTS_PER_PAGE, title = "Tag: " + tag.name, sort_column = sort_column, 
    sort_direction = sort_direction)