from app import app
import users
import questions as q
from flask import redirect, render_template, request, session, url_for, abort


#routes_questions.py
#routes_answers.py


@app.route("/all_users")
def all_users():
    user_list = users.fetch_users(True,"")
    return render_template("all_users.html", user_list = user_list)


@app.route("/search", methods = ["GET","POST"])
def search():
    
    if request.method=="GET":
        return render_template("search.html")

    if request.method=="POST":

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        options = request.form.getlist("search_option")

        if not options:
            return render_template("errors.html", message="You must select at least 1 search option")
        else:
            query = request.form["search"]
            query = "%"+query+"%"

            user_list = users.fetch_users(False,query)  if "users"      in options else None

            question_list = q.question_query(query)     if "questions"  in options else None

            answer_list   = q.answer_query(query)       if "answers"    in options else None

            return render_template(
                "result.html", 
                options=options, 
                query=query, 
                question_list=question_list,
                user_list=user_list,
                answer_list=answer_list)



@app.route("/sort_by/<question_id>", methods = ["POST"])
def sort_by(question_id):
    sort_option = request.form["sort_option"]
    return redirect(url_for("question_url", question_id = question_id, sort_option=sort_option))


@app.route("/<question_id>/<sort_option>")
def question_url(question_id,sort_option):

    question = q.fetch_question(question_id)
    answers = q.fetch_all_answers(question_id, sort_option)
    admins = [admin for admin, in  users.fetch_all_admins()]

    return render_template(
        "new.html",
        admins = admins,
        question_id = question_id,
        question = question,
        answers = answers, 
        sort_option=sort_option)



@app.route("/<question_id>/<answer_id>/<answer_points>/<sort_option>", methods =["POST"])
def give_vote(question_id, answer_id, answer_points,sort_option):
    vote_type = request.form.get("vote")
    q.vote(vote_type, answer_id, answer_points)
    return redirect(url_for("question_url", question_id = question_id,sort_option=sort_option))

@app.route("/<question_id>/<sort_option>/<answer_id>", methods = ["POST"])
def delete_answer(question_id, sort_option, answer_id):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
        
    q.delete("answers", answer_id)
    return redirect(url_for("question_url", question_id = question_id, sort_option=sort_option))

@app.route("/<question_id>", methods = ["POST"])
def delete_question(question_id):

    if session["csrf_token"] != request.form["csrf_token"]:
         abort(403)

    q.delete("user_questions", question_id)
    return render_template("success.html", message = "Question successfully deleted!")



@app.route("/edit_question/<question_id>", methods = ["POST"])
def edit_question(question_id):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
        
    question = q.fetch_question(question_id)

    question_title   = question[0]
    question_content = question[1]

    return render_template(
        "edit.html",
        question = question, 
        id = question_id, 
        question_title = question_title, 
        question_content = question_content)

@app.route("/edit_answer/<answer_id>", methods = ["POST"])
def edit_answer(answer_id):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    answer = q.fetch_answer(answer_id)
    answer_content = answer[0]

    return render_template("edit.html", id = answer_id, answer_content=answer_content)
    

@app.route("/commit_edit/<id>/<type>", methods =["POST"])
def commit_edit(id,type):

    if type =="question":

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        title = request.form["title"]
        content = request.form["question"]

        #Lisää syötteiden hallinta tähän 

        if q.commit_edit("question", id, title, content):
            return render_template("success.html", message ="Successfully Edited!")
        else:
            return render_template("errors.html", message="Failed to edit!")

    if type =="answer":

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        content = request.form["answer"]
        if q.commit_edit("answer", id, "", content):
            return render_template("success.html", message ="Successfully Edited!")
        else:
            return render_template("errors.html", message="Failed to edit!")


@app.route("/<question_id>/<sort_option>", methods =["POST"])
def post_answer(question_id, sort_option):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    answer = request.form["answer"]
    if q.save_answer(answer,question_id):
        return redirect(url_for("question_url", question_id = question_id, sort_option=sort_option))
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

        if session["csrf_token"] != request.form["csrf_token"]:
             abort(403)

        title = request.form["title"]
        question = request.form["question"]

        #if len(title) >= 5 and len(title) <= 150:

        #200 words and 1500 characters at least 5 words! 

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

    display_list = q.index_query()

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


