from flask import render_template, redirect, request, url_for
from flask_login import current_user  

from application import app, db, login_required
from application.auth.models import User
from application.tags.models import Tag
from application.games.models import Game
from application.tags.forms import TagCreationForm, TagSelectionForm

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
    if current_user.id != user.id: 
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
def tasks_delete(tag_id):
    tag = Tag.query.get(tag_id)
    if not tag: 
        return render_template("error.html", error = "Tagia ei ole olemassa")
    if tag.account_id != current_user.id:
        return render_template("error.html", error = "Et voi poistaa toisen tagia")
    
    GameTag.query.filter(GameTag.tag_id==tag_id).all().delete()
    db.session.delete(tag)
    db.session.commit()
    return redirect(url_for("tags_index", user_id=current_user.id))