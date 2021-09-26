from app import app
import users
import questions as q
from flask import redirect, render_template, request, session, url_for


@app.route("/<question_id>/<answer_id>/<answer_points>/<option>", methods =["POST"])
def giveVote(question_id, answer_id, answer_points,option):
    voteType = request.form.get("vote")
    q.vote(voteType, answer_id, answer_points)
    return redirect(url_for('questionURL', question_id = question_id,option=option))

@app.route("/<question_id>/<option>/<answer_id>", methods = ["POST"])
def deleteAnswer(question_id, option, answer_id):
    q.delete("answers", answer_id)
    return redirect(url_for('questionURL', question_id = question_id, option=option))

@app.route("/<question_id>", methods = ["POST"])
def deleteQuestion(question_id):
    q.delete("user_questions", question_id)
    return render_template("index.html", message = "Question successfully deleted!")


@app.route("/sortBy/<question_id>", methods = ["POST"])
def sortBy(question_id):
    option = request.form["option"]
    return redirect(url_for('questionURL', question_id = question_id, option=option))


@app.route("/<question_id>/<option>")
def questionURL(question_id,option):

    question = q.fetchQuestion(question_id)
    answers = q.fetchAllAnswers(question_id, option)

    return render_template("new.html", question_id = question_id, title = question[0], 
            content = question[1], username = question[2],
             time = question[3], user_id = question[4], answers = answers, option=option)



@app.route("/<question_id>/<option>", methods =["POST"])
def giveAnswer(question_id, option):
    answer = request.form["answer"]
    if q.postAnswer(answer,question_id):
        return redirect(url_for('questionURL', question_id = question_id, option=option))
    else:
        return render_template("errors.html", message="Failed to post question")



@app.route("/allquestions")
def allquestions():
    questionlist = q.fetchAllQuestions()
    return render_template("questions.html", questionlist = questionlist)

@app.route("/myquestions")
def myquestions():
    id = users.user_id()
    questionlist = q.fetchMyQuestions(id)
    return render_template("questions.html", questionlist = questionlist)


@app.route("/postquestion", methods=["GET","POST"])
def postquestion():
    if request.method == "GET":
        return render_template("postquestion.html")

    if request.method == "POST":
        title = request.form["title"]
        question = request.form["question"]
        if q.postQuestion(title, question):
            return render_template("index.html", message ="Successfully posted!")
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
            return render_template("index.html",message = "Thank you! Please login to proceed")
        else:
            return render_template("errors.html", message = "Registration failed")


@app.route("/allusers")
def allusers():
    userlist = users.fetchusers()
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
            return render_template("errors.html", message = "Wrong username or password")


@app.route("/logout")
def logout():
    del session["username"]
    return redirect("/")


