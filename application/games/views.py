from application import app, db
from flask import render_template, request
from application.games.models import Game


@app.route("/games/new")
def games_form(): 
    return render_template("games/new.html")

@app.route("/games/", methods=["POST"])
def games_create():                 
    t = Game(request.form.get("name"))
    db.session.add(t)
    db.session.commit()
    
    return "Jotain on tehty tiedoillasi ;)"
