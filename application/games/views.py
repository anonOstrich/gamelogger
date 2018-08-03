from application import app, db
from flask import render_template, request
from application.games.models import Game


@app.route("/games/new")
def games_form(): 
    return render_template("games/new.html")

@app.route("/games/", methods=["POST"])
def games_create():                 
    g = Game(request.form.get("name"), request.form.get("developer"), int(request.form.get("year")))
    db.session.add(g)
    db.session.commit()
    
    return "Peli on tallennettu järjestelmään!"
