from flask import redirect, render_template, request, url_for
from flask_login import current_user, login_required

from application import app, db
from application.reactions.forms import ReactionForm
from application.reactions.models import Reaction 

from application.reviews.models import Review


@app.route("/reaction/<review_id>", methods=["POST"])
@login_required
def reactions_create(review_id):
    # validate that review exists. Perhaps Review.exists(game_id)
    form = ReactionForm(request.form)
    if not form.validate():
        return render_template("error.html", error="Yritit jotain kavalaa")
    positive = False
    if form.positivity.data=="positive":
        positive = True
    r = Reaction(positive)
    r.account_id = current_user.id
    r.review_id = review_id
    db.session.add(r)
    db.session.commit()
    return redirect(url_for("games_view", game_id=Review.query.get(review_id).game_id))
    
