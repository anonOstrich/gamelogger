from flask import render_template, request, redirect, url_for
from flask_login import login_required

from application import app, db
from application.games.models import Game
from application.games.forms import GameForm
from application.reviews.models import Review
from application.reactions.forms import ReactionForm



@app.route("/games/new")
@login_required
def games_form():
    return render_template("games/new.html", form = GameForm())


@app.route("/games/", methods=["GET"])
def games_index(): 
    return render_template("games/list.html", games = Game.query.all(), review_numbers = Game.find_all_number_of_reviews(),
                           review_averages = Game.find_all_averages_of_reviews())


@app.route("/games/", methods=["POST"])
@login_required
def games_create():  
    form = GameForm(request.form)
    
    if not form.validate(): 
        return render_template("/games/new.html", form = form)
    
    g = Game(form.name.data, form.developer.data, form.description.data,  form.year.data)
    db.session.add(g)
    db.session.commit()
    
    return redirect(url_for("games_index"))

@app.route("/games/<game_id>", methods=["GET"])
def games_view(game_id): 
    g = Game.query.get(game_id) 
    reviews = Review.query.filter_by(game_id = game_id).all()
    form = ReactionForm()
    if not g: 
        return render_template("error.html", error = "Peliä ei ole olemassa")
    return render_template("/games/single.html", game = g, reviews = reviews, form = form )

    
@app.route("/games/<game_id>/modify", methods=["GET", "POST"])
@login_required
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
        return render_template("/games/modify.html", form = form, id=game_id)
    
    form = GameForm(request.form)
    if not form.validate():
        render_template("games/modify.html", form = form, id = game_id)
    g.name = form.name.data
    g.year = form.year.data
    g.description = form.description.data
    g.developer = form.developer.data
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/games/<game_id>/delete", methods=["POST"])
@login_required
def games_delete(game_id):
    poistettava = Game.query.get(game_id)
    db.session.query(Review).filter(Review.game_id == game_id).delete()
    db.session.delete(poistettava)
    db.session.commit()
    return redirect(url_for("index")) 


