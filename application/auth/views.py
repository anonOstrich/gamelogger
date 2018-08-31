from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user

from application import app, db, bcrypt, login_required
from application.auth.models import Role, User, UserRole
from application.auth.forms import LoginForm, RegisterForm, DescriptionForm
from application.tags.models import Tag, GameTag
from application.reviews.models import Review
from application.reactions.models import Reaction

@app.route("/auth/login/", methods = ["GET", "POST"])
def auth_login(): 
    if request.method == "GET":
        return render_template("auth/loginform.html", form = LoginForm())    
    form = LoginForm(request.form)   
    if not form.validate(): 
        return render_template("auth/loginform.html", form = form)
    
    user = User.query.filter_by(username=form.username.data).first()
    
    if not (user and user.password_matches(form.password.data)): 
        return render_template("auth/loginform.html", form = form, notfound_error = "Virheellinen käyttäjätunnus tai salasana")

    login_user(user)
    # ohjataan sinne minne oltiin menossa
    next = request.form.get("next_address")
    if next != "None": 
        return redirect(next)
    
    return redirect(url_for("index"))
          


@app.route("/auth/logout/", methods=["GET"])
def auth_logout():
    logout_user()
    next = request.args.get("next_path")
    if next: 
        return redirect(next)

    return redirect(url_for("index"))


@app.route("/auth/register/", methods = ["POST", "GET"])
def auth_register(): 
    if request.method == "GET": 
        return render_template("/auth/registerform.html", form = RegisterForm())
    
    form = RegisterForm(request.form)
    non_unique_username = User.user_exists_with_username(form.username.data)
    if (not form.validate()) or non_unique_username: 
        error_message = None
        if non_unique_username: 
            error_message = "Käyttäjätunnus " + form.username.data + " on valitettavasti varattu"

        return render_template("/auth/registerform.html", form=form, non_unique_error = error_message)
     

    user = User(form.name.data, form.username.data, form.password.data, form.description.data)
    db.session.add(user)
    db.session.commit()
    user.add_role(Role.query.filter_by(name="DEFAULT").first())

    login_user(user)

    return redirect(url_for("index"))
    

@app.route("/users/")
def users_index():

    return render_template("/auth/list.html", users = User.query.all())

@app.route("/users/<user_id>")
def users_view(user_id):
    user = User.query.get(user_id)
    if not user:
        render_template("error.html", error = "Käyttäjää ei ole olemassa")
    
    reviews = Review.query.join(User).filter(User.id == user_id).order_by("review.date_modified DESC").limit(5).all()

    tags = Tag.query.join(User).filter(User.id == user_id).order_by("tag.name ASC").all()

    return render_template("auth/single.html", user=user, tags=tags, reviews=reviews)




@app.route("/users/<user_id>/modify", methods=["GET", "POST"])
@login_required()
def users_modify(user_id): 
    user = User.query.get(user_id)
    if not user: 
        return render_template("error.html", error = "Käyttäjää ei ole olemassa")

    if current_user.id != user_id and not current_user.has_role("ADMIN"): 
        return render_template("error.html", error = "Sinulla ei ole oikeuksia muokata käyttäjän kuvausta")   
    if request.method == "GET":
        form = DescriptionForm()
        form.description.data = user.description
        return render_template("auth/modify.html", form=form, user=user )
    form = DescriptionForm(request.form)
    if not form.validate():
        return render_template("auth/modify.html", form=form, user=user)
    user.description = form.description.data
    db.session.commit()
    return redirect(url_for("users_view", user_id=user.id))