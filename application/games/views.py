from flask import render_template, request, redirect, url_for
from application import app, db
from application.games.models import Game
from application.games.forms import GameForm



@app.route("/games/new")
def games_form():
    return render_template("games/new.html", form = GameForm())


@app.route("/games/", methods=["GET"])
def games_index(): 
    return render_template("games/list.html", games = Game.query.all())

@app.route("/games/<game_id>", methods=["POST"])
def games_set_completed(game_id):
    g = Game.query.get(game_id)
    g.completed = True
    db.session.commit()
    return redirect(url_for("games_index"))

@app.route("/games/", methods=["POST"])
def games_create():  
    form = GameForm(request.form)
    g = Game(form.name.data, form.developer.data, form.developer.description,  form.year.data)
    db.session.add(g)
    db.session.commit()
    
    return redirect(url_for("games_index"))
