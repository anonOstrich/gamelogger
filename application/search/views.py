from flask import render_template, redirect, url_for, request
from flask_login import current_user
from application import app, db
from application.games.models import Game
from application.search.forms import SearchForm

@app.route("/search", methods=["GET", "POST"])
def search(): 

    if request.method == "GET":
        form = SearchForm()
        if current_user.is_authenticated: 
            form.set_tags_info(current_user)
        return render_template("search/search.html", form = form)
    
    form = SearchForm(request.form)
    if current_user.is_authenticated:
        form.set_tags_info(current_user)
    # pitäisikö tarkastaa, että ei ole lisätty tageihin jonkun muun tageja? Halutaanko estää etsiminen?

    if not form.validate():
        tag_values = form.tags.data
        if current_user.is_authenticated: 
            form.set_tags_info(current_user)
            form.tags.data = tag_values
        return render_template("search/search.html", form=form)
    
    search_parameters = {}

    # varmasti on järkevämpi tapa iteroida läpi kentät...
    print(form.genres.data)
    if form.name.data != "": 
        search_parameters["name"] = form.name.data
    
    if form.min_year.data is not None: 
        search_parameters["min_year"] = form.min_year.data
    
    if form.max_year.data is not None: 
        search_parameters["max_year"] = form.max_year.data
    
    if form.developer.data != "":
        search_parameters["developer"] = form.developer.data

    if form.genres.data:
        search_parameters["genres"] = tuple(form.genres.data)


    # Ei ainakaan vielä tarkasteta, että annetut tägit ovat ne, jotka lomakkeessa on tarjottu vaihtoedhtoiksi
    # toisin sanoen: muokkaamalla tagi-vaihtoehtojen value-kenttää, voi hakea myös muiden käyttäjien tagien perusteella
    # Koska kaikkien tagit ovat joka tapauksessa julkisia eikä tähän ominaisuuteen varmasti törmää ilman aktiivista sörkkimistä, 
    # ei liene tarpeellista estää

    if form.tags.data: 
        search_parameters["tags"] = tuple(form.tags.data)

    if form.min_average.data is not None:
        search_parameters["min_average"] = form.min_average.data
    if form.max_average.data is not None: 
        search_parameters["max_average"] = form.max_average.data
    if form.min_count.data is not None:
        search_parameters["min_count"] = form.min_count.data
    if form.max_count.data is not None: 
        search_parameters["max_count"] = form.max_count.data

    games_info = Game.find_all_info(search_parameters)
    return render_template("search/search.html", form=form, games_info = games_info)