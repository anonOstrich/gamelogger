from flask import render_template, request, redirect, url_for
from flask_login import current_user

from application import app, db, login_required
from application.games.models import Game
from application.games.forms import GameForm
from application.reviews.models import Review
from application.reactions.models import Reaction
from application.reactions.forms import ReactionForm
from application.constants import MAXIMUM_LENGTH_OF_LISTED_TITLE
from application.utilities import shorten_if_longer_than
from application.genres.models import Genre, GameGenre
from application.genres.forms import GenreSelectionForm

from application.tags.models import Tag, GameTag



@app.route("/games/new")
@login_required()
def games_form():
    genre_form = GenreSelectionForm()
    return render_template("games/new.html", game_form = GameForm(), genre_form = genre_form)


@app.route("/games/", methods=["GET"])
def games_index(): 
    # TODO:


    games_info = Game.find_all_info()
    
    return render_template("games/list.html", games_info = games_info, title="Kaikki pelit")


@app.route("/games/", methods=["POST"])
@login_required()
def games_create():  
    game_form = GameForm(request.form)
    genre_form = GenreSelectionForm(request.form)
    
    if not (game_form.validate() and genre_form.validate()): 
        return render_template("/games/new.html", game_form = game_form, genre_form = genre_form)
    

    game = Game(game_form.name.data, game_form.developer.data, game_form.description.data,
                game_form.year.data)
    db.session.add(game)
    db.session.commit()

    game.add_genres(genre_form.genre_ids.data)
    return redirect(url_for("games_index"))

@app.route("/games/<game_id>", methods=["GET"])
def games_view(game_id): 
    g = Game.query.get(game_id) 
    reviews = Review.query.filter_by(game_id = game_id).all()
    form = ReactionForm()
    if not g: 
        return render_template("error.html", error = "Peliä ei ole olemassa")
    reactions = Reaction.find_all_reactions_for_reviews_of_game(game_id)
    genres = Genre.query.join(Genre.game_genres).filter(GameGenre.game_id==game_id).all()

    tags = []
    if current_user.is_authenticated:
        tags = Tag.query.join(Tag.game_tags).filter(Tag.account_id==current_user.id, GameTag.game_id == game_id)
    return render_template("/games/single.html", game = g, reviews = reviews, form = form,
                             reactions = reactions, genres = genres, tags = tags)

    
@app.route("/games/<game_id>/modify", methods=["GET", "POST"])
@login_required(role="ADMIN")
def games_modify(game_id):
    g = Game.query.get(game_id)
    if not g: 
        return render_template("error.html", error = "Peliä ei ole olemassa")
    if request.method == "GET":
        form = GameForm()
        form.name.data = g.name
        form.year.data = g.year
        form.description.data = g.description
        form.developer.data = g.developer

        genre_form = GenreSelectionForm()
        genre_ids = [game_genre.genre_id for game_genre in GameGenre.query.filter(GameGenre.game_id == game_id)]
        genre_form.genre_ids.data = genre_ids
        return render_template("/games/modify.html", form = form, id  = game_id, genre_form = genre_form)
    
    form = GameForm(request.form)
    genre_form = GenreSelectionForm(request.form)
    if not (form.validate() and genre_form.validate()):
        render_template("games/modify.html", form = form, genre_form = genre_form, id = game_id)
    g.name = form.name.data
    g.year = form.year.data
    g.description = form.description.data
    g.developer = form.developer.data
    new_genres = genre_form.genre_ids.data
    g.update_genres(new_genres)

    return redirect(url_for("games_view", game_id = game_id))

@app.route("/games/<game_id>/delete", methods=["POST"])
@login_required(role="ADMIN")
def games_delete(game_id):
    poistettava = Game.query.get(game_id)
    if not poistettava: 
        return render_template("error.html", error = "Peliä ei ole tietokannassa")
    Reaction.delete_reactions_relating_to_game(game_id)
    Review.query.filter(Review.game_id == game_id).delete()

    # poistetaan vain liitostaulun turhat tiedot, mutta genre jää
    GameGenre.query.filter(GameGenre.game_id == game_id).delete()
    db.session.delete(poistettava)
    db.session.commit()
    return redirect(url_for("games_index")) 


