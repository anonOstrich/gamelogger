from flask import redirect, render_template, request, url_for

from application import app, db, login_required
from application.genres.models import Genre, GameGenre
from application.genres.forms import GenreCreationForm
from application.games.models import Game
from application.constants import GAME_RESULTS_PER_PAGE
from application.utilities import parse_to_int

@app.route("/genres", methods = ["GET"])
def genres_index(page_number = 1): 
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

@app.route("/genres/<genre_id>/modify", methods = ["GET", "POST"])
@login_required("ADMIN")
def genres_modify(genre_id): 
    genre = Genre.query.get(genre_id)
    if not genre: 
        return render_template("error.html", error = "Genreä ei ole olemassa")

    if request.method == "GET":
        form = GenreCreationForm()
        form.name.data = genre.name
        return render_template("/genres/modify.html", form = form, genre = genre)


    form = GenreCreationForm(request.form)
    if not form.validate(): 
        return render_template("/genres/modify.html", form = form, genre = genre)
    
    genre.name = form.name.data
    db.session.commit()
    return redirec(url_for("genres_index"))

@app.route("/genres/<genre_id>/delete")
@login_required("ADMIN")
def genres_delete(genre_id):
    genre = Genre.query.get(genre_id)
    if not genre: 
        return render_template("error.html", error = "Genreä ei ole olemassa")

    GameGenre.query.filter(GameGenre.genre_id == genre.id).delete()
    db.session.delete(genre)
    db.session.commit()
    return redirect(url_for("genres_index"))

# Näkymä kaikille yhden genren peleille
@app.route("/genres/<genre_id>", methods=["GET"])
@app.route("/genres/<genre_id>/page/<page_number>", methods=["GET"])
def genres_view(genre_id, page_number = 1, sort_column = 0, sort_direction = "ASC"): 
    genre = Genre.query.filter_by(id=genre_id).first()
    if genre is None: 
        return render_template("error.html", error = "Genreä ei ole olemassa")

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


    games_info = Game.find_all_info_sorted({"genres": [genre.id]}, page_number = page_number, 
    order_column = columns[sort_column], order_direction = sort_direction)
    base_url = "/genres/" + str(genre_id) + "/page"
    
    return render_template("games/list.html", games_info = games_info, title = ("Genre: " + genre.name),
     page_number = page_number, last_page = len(games_info) < GAME_RESULTS_PER_PAGE,  base_url = base_url
     , sort_column = sort_column, sort_direction = sort_direction)