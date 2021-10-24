from app import app
import users as users
import fetch as fetch
import queries as queries
import thread_functions as TF
from flask import redirect, render_template, request, session, url_for, abort


@app.route("/sort_by/<question_id>", methods = ["POST"])
def sort_by(question_id):
    sort_option = request.form["sort_option"]
    return redirect(url_for("question_thread", question_id = question_id, sort_option=sort_option))

@app.route("/<question_id>/<sort_option>")
def question_thread(question_id,sort_option):

    question = fetch.fetch_question(question_id)
    answers = fetch.fetch_all_answers(question_id, sort_option)
    admins = [admin for admin, in  fetch.fetch_all_admins()]

    solved_answer = fetch.fetch_solved_answer(question_id)

    solved_answer = solved_answer[0] if solved_answer != [] else solved_answer

    return render_template(
        "question_thread.html",
        admins = admins,
        question_id = question_id,
        question = question,
        answers = answers, 
        sort_option=sort_option,
        solved_answer=solved_answer)

@app.route("/solved_warning/<question_id>")
def solved_warning(question_id):

    return render_template("solved_warning.html", question_id=question_id)


@app.route("/solved_confirmation/<question_id>/<sort_option>/<answer_id>", methods =["GET","POST"])
def solved_confirmation(question_id,sort_option,answer_id):

    if request.method == "GET" and answer_id == "none":

        answers = fetch.fetch_all_answers(question_id, sort_option)
        admins = [admin for admin, in  fetch.fetch_all_admins()]

        return render_template(
            "solved_confirmation.html",
            admins=admins, 
            answers=answers,
            question_id=question_id,
            sort_option=sort_option)

    if request.method =="POST":        

        if session["csrf_token"] != request.form["csrf_token"]:
            abort(403)

        TF.solve_question(question_id, answer_id)

        return render_template(
            "success.html",
             message="Congratulations on choosing the best answer to your question :)!")

@app.route("/<question_id>/<answer_id>/<answer_points>/<sort_option>", methods =["POST"])
def give_vote(question_id, answer_id, answer_points,sort_option):
    vote_type = request.form.get("vote")
    TF.vote(vote_type, answer_id, answer_points)
    return redirect(url_for("question_thread", question_id = question_id,sort_option=sort_option))


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

    if TF.post_answer(answer,question_id):
        return redirect(url_for("question_thread", question_id = question_id, sort_option=sort_option))
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

        if TF.post_question(title, question):
            return render_template(
                "success.html", 
                message ="Successfully posted!")
        else:
            return render_template(
                "errors.html",
                 message="Failed to post question")



