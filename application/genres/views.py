from flask import redirect, render_template, request, url_for

from application import app, db, login_required
from application.genres.models import Genre
from application.genres.forms import GenreCreationForm


@app.route("/genres", methods = ["GET"])
@login_required(role="ADMIN")
def genres_index(): 
    return render_template("genres/list.html", genres = Genre.query.all(), form = GenreCreationForm())

@app.route("/genres", methods = ["POST"])
@login_required(role="ADMIN")
def genres_create(): 
    form = GenreCreationForm(request.form)
    if not form.validate():
        return render_template("genres/list.html", genres = Genre.query.all(), form=form)

    g = Genre(form.name.data)
    if Genre.query.filter_by(name=g.name).first():
        return render_template("genres/list.html", genres = Genre.query.all(),
                                error = "Samaa genreä ei voi lisätä kahdesti", form=form)

    db.session.add(g)
    db.session.commit()
    return redirect(url_for("genres_index"))