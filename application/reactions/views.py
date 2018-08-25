from flask import redirect, render_template, request, url_for
from flask_login import current_user

from application import app, db, login_required
from application.reactions.forms import ReactionForm
from application.reactions.models import Reaction 

from application.reviews.models import Review


@app.route("/reaction/<review_id>", methods=["POST"])
@login_required()
def reactions_create(review_id):
    review_exists = Review.query.filter_by(id=review_id).first() is not None
    if not review_exists: 
        return render_template("error.html", error = "Arviota ei ole olemassa.")

    form = ReactionForm(request.form)
    if not form.validate():
        return redirect(url_for("games_view", game_id=Review.query.get(review_id).game_id))
    r = Reaction(form.positivity.data)
    r.account_id = current_user.id
    r.review_id = review_id
    db.session.add(r)
    db.session.commit()
    return redirect(url_for("games_view", game_id=Review.query.get(review_id).game_id))
    

