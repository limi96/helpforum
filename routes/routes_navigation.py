from app import app
import users as users
import fetch as fetch
import queries as queries
import thread_functions as TF
from flask import redirect, render_template, request, session, url_for, abort

@app.route("/browse/")
def browse():
    return render_template("browse.html")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")

    if request.method =="POST":
        #add new user with username and password    
        username = request.form["username"]
        password = request.form["password"]
        password_repeat = request.form["password_repeat"]


        if password != password_repeat:
            return render_template("errors.html", message="Passwords do not match")

        if len(username) > 1 and len(username) <= 15:
            if users.register(username, password):
                return render_template(
                    "success.html",
                    message = "Thank you! You are now logged in!")
            else:
                return render_template(
                    "errors.html", 
                    message = "Registration failed: User already exists")
        return render_template(
            "errors.html", 
            message="Registration failed: Username not within 1-15 characters")

@app.route("/")
def index():    

    display_list = queries.index_query()

    return render_template("index.html", display_list = display_list)


@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method =="GET":
        return render_template("login.html")

    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            return redirect("/")
        else:
            return render_template("errors.html", message = "Wrong username or password")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


