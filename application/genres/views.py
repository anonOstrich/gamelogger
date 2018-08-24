from flask import redirect, render_template, request, url_for

from application import app, db, login_required
from application.genres.models import Genre, GameGenre
from application.genres.forms import GenreCreationForm
from application.games.models import Game

@app.route("/genres", methods = ["GET"])
def genres_index(): 
    sorted_genres = Genre.find_genres_sorted_by_number_of_games()
    return render_template("genres/list.html", genres = sorted_genres, form = GenreCreationForm())

@app.route("/genres", methods = ["POST"])
@login_required(role="ADMIN")
def genres_create(): 
    form = GenreCreationForm(request.form)
    if not form.validate():
        return render_template("genres/list.html", genres = Genre.query.all(), form=form)

    g = Genre(form.name.data)
    if Genre.query.filter_by(name=g.name).first():
        return render_template("genres/list.html", genres = Genre.query.all(),
                                error = "Samaa genreä ei voi lisätä kahdesti", form=form)

    db.session.add(g)
    db.session.commit()
    return redirect(url_for("genres_index"))


# Näkymä kaikille yhden genren peleille
@app.route("/genres/<genre_id>", methods=["GET"])
def genres_view(genre_id): 
    genre = Genre.query.filter_by(id=genre_id).first()

    if genre is None: 
        return render_template("error.html", error = "Genreä ei ole olemassa")
    
    return render_template("games/list.html", games = Game.query.join(Game.game_genres).filter(GameGenre.genre_id == genre_id).all(),
                            review_numbers = Game.find_numbers_of_reviews_for_genre(genre_id),
                        review_averages = Game.find_averages_of_reviews_for_genre(genre_id), title = ("Genre: " + genre.name))