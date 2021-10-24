from app import app
import users
import questions as q
from flask import redirect, render_template, request, session, url_for, abort

#routes_questions.py
#routes_answers.py

@app.route("/user_profile/<username>")
def user_profile(username):

    user_info = users.fetch_users(False, username,"")[0]
    recent_questions = q.fetch_recent_questions(username)
    recent_answers = q.fetch_recent_answers(username)

    return render_template(
        "user_profile.html",
        user_info=user_info,
        recent_questions=recent_questions,
        recent_answers=recent_answers)

@app.route("/all_users/<sort_option>", methods=["GET","POST"])
def all_users(sort_option):
    if request.method == "GET":

        user_list = users.fetch_users(True,"",sort_option)
        return render_template("all_users.html",sort_option=sort_option, user_list = user_list)

    if request.method == "POST":
        sort_option = request.form["sort_option"]
    
        return redirect(url_for(
            "all_users", sort_option=sort_option))
    

@app.route("/user_answers/<username>/<sort_option>", methods=["GET","POST"])
def user_answers(username,sort_option):

    if request.method == "GET":
        answer_list = q.fetch_my_answers(username, sort_option)

        return render_template(
            "user_answers.html", 
            username=username, 
            answer_list=answer_list, 
            sort_option=sort_option)

    if request.method == "POST":
        sort_option = request.form["sort_option"]
    
        return redirect(url_for(
            "user_answers", username =username, sort_option=sort_option))

@app.route("/user_questions/<username>/<sort_option>", methods=["GET","POST"])
def user_questions(username,sort_option):

    if request.method == "GET":

        question_list = q.fetch_my_questions(username,sort_option)
        message = username + "'s questions"
        return render_template(
            "user_questions.html",
            sort_option=sort_option, 
            username=username, 
            question_list = question_list, 
            message=message)

    if request.method == "POST":
        sort_option = request.form["sort_option"]
        return redirect(url_for(
            "user_questions", username =username, sort_option=sort_option))


@app.route("/solved_questions/<sort_option>", methods=["GET","POST"])
def solved_questions(sort_option):
    if request.method == "GET":
        question_list = q.fetch_solved_questions(sort_option)
        return render_template(
            "solved_questions.html", 
            sort_option=sort_option,
            question_list = question_list, 
            message="Solved questions")

    if request.method == "POST":
        sort_option = request.form["sort_option"]
        return redirect(url_for(
            "solved_questions", sort_option=sort_option))


@app.route("/all_questions/<sort_option>", methods=["GET","POST"])
def all_questions(sort_option):
    if request.method == "GET":
        question_list = q.fetch_all_questions(sort_option)
        return render_template(
            "all_questions.html", 
            sort_option=sort_option,
            question_list = question_list, 
            message="All questions")

    if request.method == "POST":
        sort_option = request.form["sort_option"]
        return redirect(url_for(
            "all_questions", sort_option=sort_option))

@app.route("/sort_by/<question_id>", methods = ["POST"])
def sort_by(question_id):
    sort_option = request.form["sort_option"]
    return redirect(url_for("question_url", question_id = question_id, sort_option=sort_option))

@app.route("/<question_id>/<sort_option>")
def question_url(question_id,sort_option):

    question = q.fetch_question(question_id)
    answers = q.fetch_all_answers(question_id, sort_option)
    admins = [admin for admin, in  users.fetch_all_admins()]

    solved_answer = q.fetch_solved_answer(question_id)

    solved_answer = solved_answer[0] if solved_answer != [] else solved_answer

    return render_template(
        "new.html",
        admins = admins,
        question_id = question_id,
        question = question,
        answers = answers, 
        sort_option=sort_option,
        solved_answer=solved_answer)

@app.route("/browse/")
def browse():
    return render_template("browse.html")


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

            if not query:
                return render_template("errors.html", message="You must have at least 1 search word!")

            query = "%"+query+"%"

            posted_by   = request.form["posted_by"]
            posted_by = request.form["posted_by"]

            user_list     = users.fetch_users(False,query,"")   if "users"      in options else None
            answer_list   = q.answer_query(query,posted_by)     if "answers"    in options else None
            question_list = q.question_query(query,posted_by)   if "questions"  in options else None

            return render_template(
                "result.html",
                options=options, 
                query=query, 
                question_list=question_list,
                user_list=user_list,
                answer_list=answer_list)

@app.route("/solved_warning/<question_id>")
def solved_warning(question_id):

    return render_template("solved_warning.html", question_id=question_id)


@app.route("/solved_confirmation/<question_id>/<sort_option>/<answer_id>", methods =["GET","POST"])
def solved_confirmation(question_id,sort_option,answer_id):

    if request.method == "GET" and answer_id == "none":

        answers = q.fetch_all_answers(question_id, sort_option)
        admins = [admin for admin, in  users.fetch_all_admins()]

        return render_template(
            "solved_confirmation.html",
            admins=admins, 
            answers=answers,
            question_id=question_id,
            sort_option=sort_option)

    if request.method =="POST":        

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        q.solve_question(question_id, answer_id)

        return render_template(
            "success.html",
             message="Congratulations on choosing the best answer to your question :)!")









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

    return render_template(
        "edit_question.html",
        question = question, 
        id = question_id, 
        question_title = question.question_title, 
        question_content = question.question_content)


@app.route("/edit_answer/<answer_id>", methods = ["POST"])
def edit_answer(answer_id):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
    
    answer = q.fetch_answer(answer_id)
    answer_content = answer.answer_content

    return render_template("edit_answer.html", id = answer_id, answer_content=answer_content)
    

@app.route("/commit_edit/<id>/<type>", methods =["POST"])
def commit_edit(id,type):

    if type =="question":

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        title = request.form["title"]
        content = request.form["question"]

        words = content.split()

        if len(title) < 5 or len(title) > 150:
            return render_template(
            "errors.html", 
            message="Title must be within 5-150 characters")

        if len(words) < 5 or len(words) > 200 or len(content) > 2000:
            return render_template(
                "errors.html", 
                message="The description must be within 5-200 words and no longer than 2000 characters")

        if q.commit_edit("question", id, title, content):
            return render_template("success.html", message ="Successfully Edited!")
        else:
            return render_template("errors.html", message="Failed to edit!")

    if type =="answer":

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        content = request.form["answer"]
        words = content.split()

        if len(words) < 2 or len(words) > 100 or len(content) > 2000:
            return render_template(
            "errors.html", 
            message="The answer must be within 2-100 words and no longer than 2000 characters")

        if q.commit_edit("answer", id, "", content):
            return render_template("success.html", message ="Successfully Edited!")
        else:
            return render_template("errors.html", message="Failed to edit!")


@app.route("/<question_id>/<sort_option>", methods =["POST"])
def post_answer(question_id, sort_option):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    answer = request.form["answer"]

    words = answer.split()

    if len(words) < 2 or len(words) > 100 or len(answer) > 2000:
        return render_template(
            "errors.html", 
            message="The answer must be within 2-100 words and no longer than 2000 characters")

    if q.post_answer(answer,question_id):
        return redirect(url_for("question_url", question_id = question_id, sort_option=sort_option))
    else:
        return render_template("errors.html", message="Failed to post question")



@app.route("/post_question", methods=["GET","POST"])
def post_question():

    if request.method == "GET":
        return render_template("post_question.html")

    if request.method == "POST":

        if session["csrf_token"] != request.form["csrf_token"]:
             abort(403)

        title = request.form["title"]
        question = request.form["question"]

        words = question.split()

        if len(title) < 5 or len(title) > 150:
            return render_template(
                "errors.html", 
                message="Title must be within 5-150 characters")

        if len(words) < 5 or len(words) > 200 or len(question) > 2000:
            return render_template(
                "errors.html", 
                message="The description must be within 5-200 words and no longer than 2000 characters")

        if q.post_question(title, question):
            return render_template(
                "success.html", 
                message ="Successfully posted!")
        else:
            return render_template(
                "errors.html",
                 message="Failed to post question")


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


