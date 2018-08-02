from application import app 
from flask import render_template, request

@app.route("/movies/new")
def movies_form(): 
    return render_template("movies/new.html")

@app.route("/movies/", methods=["POST"])
def movies_create():   
    print("Nimi:" + request.form.get("name"))
    print("Ohjaaja:" + request.form.get("director"))
    print("Ilmestymisvuosi:" + request.form.get("year"))
    print("Kesto" + request.form.get("runtime"))
    return "HEHE :))"
