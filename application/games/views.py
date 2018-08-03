from application import app, db
from flask import render_template, request, redirect, url_for
from application.games.models import Game


@app.route("/games/new")
def games_form(): 
    return render_template("games/new.html")


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
    g = Game(request.form.get("name"), request.form.get("developer"), request.form.get("description"),  int(request.form.get("year")))
    db.session.add(g)
    db.session.commit()
    
    return redirect(url_for("games_index"))
