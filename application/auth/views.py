from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user

from application import app, db, bcrypt
from application.auth.models import Role, User, UserRole
from application.auth.forms import LoginForm, RegisterForm


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
          


@app.route("/auth/logout")
def auth_logout():
    logout_user()
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
        form.username.data = ""
        return render_template("/auth/registerform.html", form=form, non_unique_error = error_message)
     

    user = User(form.name.data, form.username.data, form.password.data)
    db.session.add(user)
    db.session.commit()
    user.add_role(Role.query.filter_by(name="DEFAULT").first())

    return redirect(url_for("index"))
    