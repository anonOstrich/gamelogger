from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.reviews.models import Review 
from application.reactions.models import Reaction
from application.reviews.forms import ReviewForm
from application.games.models import Game


@app.route("/review/<game_id>", methods=["GET", "POST"])
@login_required()
def reviews_create(game_id):
    form = ReviewForm(request.form)
    game = Game.query.get(game_id)
    if not game:
        return render_template("error.html", error = "Peliä ei ole olemassa")    
    
    if request.method =="GET":
        return render_template("reviews/new.html", form = ReviewForm(), game = Game.query.get(game_id))
    
    if not form.validate(): 
        return render_template("reviews/new.html", form=form, game = game)
   
    if current_user.has_reviewed(game):
        return render_template("error.html", error="Et voi arvioida samaa peliä uudelleen")
    
    review = Review(form.text.data, form.points.data)
    review.game_id = game_id
    review.account_id = current_user.id
    db.session().add(review)
    db.session().commit()    
    return redirect(url_for("games_view", game_id = game_id))


@app.route("/review/<review_id>/modify", methods=["GET", "POST"])
@login_required()
def reviews_modify(review_id):
    r = Review.query.get(review_id)
    if not r: 
        return render_template("error.html", error = "Arvostelua ei löydy tietokannasta")
    if not current_user.is_allowed_to_edit_review(r):
        return render_template("error.html", error = "Sinulla ei ole muokkaamisoikeutta")

    form = ReviewForm(request.form)   
    if request.method == "GET": 
        form.text.data = r.text
        form.points.data = r.points
        return render_template("reviews/modify.html", form = form, game = Game.query.get(r.game_id), review_id = review_id)

    if not form.validate():
        return render_template("reviews/modify.html", form = form, game = Game.query.get(r.game_id), review_id = review_id)

    r.text = form.text.data
    r.points = form.points.data
    db.session.commit()
    return redirect(url_for("games_view", game_id = r.game_id))


@app.route("/review/<review_id>/delete", methods = ["GET"])
@login_required("ADMIN")
def reviews_delete(review_id):
    review = Review.query.get(review_id)
    if not review:
        return render_template("error.html", error = "Arvostelua ei ole olemassa")
    Reaction.query.filter(Reaction.review_id == review.id).delete()
    game_id = review.game_id
    db.session.delete(review)
    db.session.commit()
    return redirect(url_for("games_view", game_id = game_id))


