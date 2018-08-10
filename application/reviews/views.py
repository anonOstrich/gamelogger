from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from application import app, db
from application.reviews.models import Review 
from application.reviews.forms import ReviewForm
from application.games.models import Game


@app.route("/review/<game_id>", methods=["POST"])
@login_required
def reviews_create(game_id):
    form = ReviewForm(request.form)
    game = Game.query.get(game_id)
    if not game:
        return render_template("error.html", error = "Peliä ei ole olemassa! Palaa etusivulle ja yritä uudelleen")    
    
    if not form.validate(): 
        return render_template("reviews/new.html", form=form, game = game)
   
    
    review = Review(form.text.data, form.points.data)
    review.game_id = game_id
    review.account_id = current_user.id
    db.session().add(review)
    db.session().commit()    
    return redirect(url_for("index"))


@app.route("/review/<game_id>", methods=["GET"])
@login_required
def reviews_show(game_id):
    return render_template("reviews/new.html", form = ReviewForm(), game = Game.query.get(game_id))
    
