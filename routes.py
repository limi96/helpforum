from app import app
import users
import questions as q

from flask import redirect, render_template, request, session

@app.route("/<question_id>")
def questionURL():
    return render_template("new.html")

@app.route("/allquestions")
def allquestions():
    questionlist = q.fetchAllQuestions()
    return render_template("allquestions.html", questionlist = questionlist)

@app.route("/myquestions")
def myquestions():
    id = users.user_id()
    questionlist = q.fetchMyQuestions(id)
    return render_template("myquestions.html", questionlist = questionlist)

@app.route("/postquestion", methods=["GET","POST"])
def postquestion():
    if request.method == "GET":
        return render_template("postquestion.html")

    if request.method == "POST":
        title = request.form["title"]
        question = request.form["question"]
        if q.post(title, question):
            return redirect("/")
        else:
            return render_template("errors.html", message="Failed to post question")

@app.route("/register", methods = ["GET", "POST"])
def register():
    if request.method =="GET":
        return render_template("register.html")

    if request.method =="POST":
        #add new user with username and password    
        username = request.form["username"]
        password = request.form["password"]
        passwordrepeat = request.form["passwordrepeat"]

        if password != passwordrepeat:
            return render_template("errors.html", message="Passwords do not match")
        if users.register(username, password):
            return redirect("/")
            #return render_template("registrationsuccess.html", username = username)
        else:
            return render_template("errors.html", message = "Registration failed")


@app.route("/allusers")
def allusers():
    userlist = users.fetchusers()
    print(userlist)
    return render_template("allusers.html", userlist = userlist)


@app.route("/")
def index():    
    return render_template("index.html")









@app.route("/login", methods = ["GET","POST"])
def login():
    if request.method =="GET":
        return render_template("login.html")

    if request.method =="POST":
        username = request.form["username"]
        password = request.form["password"]

        if users.login(username, password):
            session["username"] = username
            return redirect("/")
        else:
            print("I'm here")
            return render_template("errors.html", message = "Wrong username or password")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")



            

@app.route("/page1")
def page1():
    return "Tämä on sivu 1"

@app.route("/form")
def form():
    return render_template("form.html")

@app.route("/result", methods=["POST"])
def result():
    return render_template("result.html",name=request.form["name"])

@app.route("/page/<int:abc>")
def page(abc):
    return "Tämä on sivu " + str(abc)

