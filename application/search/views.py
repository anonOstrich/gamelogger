from flask import render_template, redirect, url_for, request
from flask_login import current_user
from application import app, db
from application.games.models import Game
from application.search.forms import SearchForm

@app.route("/search", methods=["GET", "POST"])
def search(): 
    form = SearchForm()
    if request.method == "GET":
        form.set_genre_info()
        if current_user.is_authenticated: 
            form.set_tags_info(current_user)
        return render_template("search/search.html", form = form)
    
    form = SearchForm(request.form)

    # pitäisikö tarkastaa, että ei ole lisätty tageihin jonkun muun tageja? Halutaanko estää etsiminen?

    if not form.validate():
        #jos tällä välin on lisätty genrejä/tägejä... epätodennäköistähän tämä kyllä on
        tag_values = form.tags.data
        genre_values = form.genres.data
        form.set_genre_info()
        form.genres.data = genre_values
        if current_user.is_authenticated: 
            form.set_tags_info(current_user)
            form.tags.data = tag_values
        return render_template("search/search.html", form=form)
    

    games = Game.query.all()
    return render_template("search/search.html", form=form, games=games)