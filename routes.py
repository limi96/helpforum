from app import app
import users
import questions as q
from flask import redirect, render_template, request, session, url_for

@app.route("/<question_id>/<answer_id>/<answer_points>/<sort_option>", methods =["POST"])
def give_vote(question_id, answer_id, answer_points,sort_option):
    vote_type = request.form.get("vote")
    q.vote(vote_type, answer_id, answer_points)
    return redirect(url_for('question_url', question_id = question_id,sort_option=sort_option))

@app.route("/<question_id>/<sort_option>/<answer_id>", methods = ["POST"])
def delete_answer(question_id, sort_option, answer_id):
    q.delete("answers", answer_id)
    return redirect(url_for('question_url', question_id = question_id, sort_option=sort_option))

@app.route("/<question_id>", methods = ["POST"])
def delete_question(question_id):
    q.delete("user_questions", question_id)
    return render_template("success.html", message = "Question successfully deleted!")

@app.route("/sort_by/<question_id>", methods = ["POST"])
def sort_by(question_id):
    sort_option = request.form["sort_option"]
    return redirect(url_for('question_url', question_id = question_id, sort_option=sort_option))


@app.route("/<question_id>/<sort_option>")
def question_url(question_id,sort_option):

    question = q.fetch_question(question_id)
    answers = q.fetch_all_answers(question_id, sort_option)

    return render_template("new.html", question_id = question_id, title = question[0], 
            content = question[1], username = question[2],
             time = question[3], user_id = question[4], answers = answers, sort_option=sort_option)

@app.route("/<question_id>/<sort_option>", methods =["POST"])
def post_answer(question_id, sort_option):
    answer = request.form["answer"]
    if q.save_answer(answer,question_id):
        return redirect(url_for('question_url', question_id = question_id, sort_option=sort_option))
    else:
        return render_template("errors.html", message="Failed to post question")

@app.route("/all_questions")
def all_questions():
    question_list = q.fetch_all_questions()
    return render_template("questions.html", question_list = question_list)

@app.route("/my_questions")
def my_questions():
    id = users.user_id()
    question_list = q.fetch_my_questions(id)
    return render_template("questions.html", question_list = question_list)

@app.route("/post_question", methods=["GET","POST"])
def post_question():
    if request.method == "GET":
        return render_template("post_question.html")

    if request.method == "POST":
        title = request.form["title"]
        question = request.form["question"]

        #if len(title) >= 2 and len(title) <= 150:

        #Description length 500 

        if q.post_question(title, question):
            return render_template("success.html", message ="Successfully posted!")
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
        password_repeat = request.form["password_repeat"]

        if password != password_repeat:
            return render_template("errors.html", message="Passwords do not match")

        if len(username) > 1 and len(username) <= 50:
            if users.register(username, password):
                return render_template("success.html",message = "Thank you! Please login to proceed")
            else:
                return render_template("errors.html", message = "Registration failed: User already exists")
        return render_template("errors.html", message="Registration failed: Username not within 1-50 characters")

@app.route("/all_users")
def all_users():
    user_list = users.fetch_users()
    return render_template("all_users.html", user_list = user_list)


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


