from app import app
import users as users
import fetch as fetch
import queries as queries
import thread_functions as TF
from flask import redirect, render_template, request, session, url_for, abort

@app.route("/user_profile/<username>")
def user_profile(username):

    user_info = queries.user_query(username)[0]
    recent_questions = fetch.fetch_recent_questions(username)
    recent_answers = fetch.fetch_recent_answers(username)

    return render_template(
        "user_profile.html",
        user_info=user_info,
        recent_questions=recent_questions,
        recent_answers=recent_answers)

@app.route("/user_answers/<username>/<sort_option>", methods=["GET","POST"])
def user_answers(username,sort_option):

    if request.method == "GET":
        answer_list = fetch.fetch_my_answers(username, sort_option)

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

        question_list = fetch.fetch_my_questions(username,sort_option)
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
