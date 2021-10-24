from app import app
import users as users
import fetch as fetch
import queries as queries
import thread_functions as TF
from flask import redirect, render_template, request, session, url_for, abort

@app.route("/<question_id>/<sort_option>/<answer_id>", methods = ["POST"])
def delete_answer(question_id, sort_option, answer_id):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)

    TF.delete("answers", answer_id)
    return redirect(url_for("question_thread", question_id = question_id, sort_option=sort_option))

@app.route("/<question_id>", methods = ["POST"])
def delete_question(question_id):

    if session["csrf_token"] != request.form["csrf_token"]:
         abort(403)

    TF.delete("user_questions", question_id)
    return render_template("success.html", message = "Question successfully deleted!")


@app.route("/edit_question/<question_id>", methods = ["POST"])
def edit_question(question_id):

    if session["csrf_token"] != request.form["csrf_token"]:
        abort(403)
        
    question = fetch.fetch_question(question_id)

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
    
    answer = fetch.fetch_answer(answer_id)
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

        if TF.commit_edit("question", id, title, content):
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

        if TF.commit_edit("answer", id, "", content):
            return render_template("success.html", message ="Successfully Edited!")
        else:
            return render_template("errors.html", message="Failed to edit!")