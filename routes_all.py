from app import app
import users as users
import fetch as fetch
import queries as queries
import thread_functions as TF
from flask import redirect, render_template, request, session, url_for, abort


@app.route("/all_users/<sort_option>", methods=["GET","POST"])
def all_users(sort_option):
    if request.method == "GET":

        user_list = fetch.fetch_all_users(sort_option)

        return render_template("all_users.html",sort_option=sort_option, user_list = user_list)

    if request.method == "POST":
        sort_option = request.form["sort_option"]
    
        return redirect(url_for(
            "all_users", sort_option=sort_option))

@app.route("/solved_questions/<sort_option>", methods=["GET","POST"])
def solved_questions(sort_option):
    if request.method == "GET":
        question_list = fetch.fetch_solved_questions(sort_option)
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
        question_list = fetch.fetch_all_questions(sort_option)
        return render_template(
            "all_questions.html", 
            sort_option=sort_option,
            question_list = question_list, 
            message="All questions")

    if request.method == "POST":
        sort_option = request.form["sort_option"]
        return redirect(url_for(
            "all_questions", sort_option=sort_option))


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

            user_list     = queries.user_query(query)                 if "users"      in options else None
            answer_list   = queries.answer_query(query,posted_by)     if "answers"    in options else None
            question_list = queries.question_query(query,posted_by)   if "questions"  in options else None

            return render_template(
                "result.html",
                options=options, 
                query=query, 
                question_list=question_list,
                user_list=user_list,
                answer_list=answer_list)

