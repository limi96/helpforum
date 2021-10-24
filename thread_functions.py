from db import db
import users

def solve_question(question_id, answer_id):

    sql =   "INSERT INTO solved (question_id, answer_id, solved_time) VALUES (:question_id, :answer_id, NOW())"
    db.session.execute(sql, {"question_id":question_id, "answer_id":answer_id})
    db.session.commit()

    sql =   "SELECT question_title FROM user_questions WHERE id =:question_id"
    result = db.session.execute(sql,{"question_id":question_id})

    old_title = result.fetchone().question_title
    new_title = "[SOLVED] " + old_title

    sql =   "UPDATE user_questions SET question_title=:new_title WHERE id =:question_id"
    db.session.execute(sql, {"new_title":new_title,"question_id":question_id})
    db.session.commit()

def vote(voteType, answer_id, answer_points):
    user_id = users.user_id()

    #First check if user is in points
    sql =   "SELECT user_id FROM points P WHERE P.user_id = :user_id AND P.answer_id =:answer_id"
    result = db.session.execute(sql, {"user_id":user_id, "answer_id":answer_id})
    check = False

    for i in result: 
        if (i[0] == user_id): 
            check = True
            break

    if check: return False

    #If not in points, count vote
    insert_points = int(answer_points)+1 if (voteType == "Upvote!") else int(answer_points)-1

    sql = "INSERT INTO points (result, answer_id, user_id) VALUES (:result, :answer_id, :user_id)" 
    db.session.execute(sql, {"result":insert_points, "answer_id":answer_id, "user_id":user_id })
    db.session.commit()

    sql = "UPDATE answers SET answer_points=:insert_points WHERE id =:answer_id"
    db.session.execute(sql, {"insert_points":insert_points, "answer_id":answer_id})
    db.session.commit()

    return True
    

def delete(type, id):
    sql = "DELETE FROM "

    if type =="answers":         sql += type
    if type =="user_questions":  sql += type       

    sql += " WHERE id =:id"

    db.session.execute(sql, {"id":id})
    db.session.commit()

def post_question(title, question):
    user_id = users.user_id()

    if user_id == 0:
        return False    

    sql =   "INSERT INTO user_questions (question_title, question_content, user_id, send_time)"\
            "VALUES (:question_title, :question_content, :user_id, NOW())"
    db.session.execute(sql, {"question_title":title, "question_content":question, "user_id":user_id})
    db.session.commit()

    return True

def post_answer(answer, question_id):
    user_id = users.user_id()
    points = 0

    if user_id == 0:
        return False

    sql =   "INSERT INTO answers (answer_content, answer_points, question_id, user_id, send_time) "\
            "VALUES (:answer_content, :answer_points, :question_id, :user_id, NOW())"

    db.session.execute(sql, {"answer_content":answer,
                            "answer_points":points,
                            "question_id":question_id,
                            "user_id":user_id })
    db.session.commit()

    return True


def commit_edit(type, id, title, content):
    
    if type=="question":

        sql =   "UPDATE user_questions " \
                "SET question_content=:content, question_title=:title, edited_time=NOW() "\
                "WHERE id=:id"
        db.session.execute(sql, {"title":title, "content":content, "id":id})
        db.session.commit()
        return True
        
    if type=="answer":

        sql =   "UPDATE answers "\
                "SET answer_content=:content, edited_time=NOW() "\
                "WHERE id=:id"
        db.session.execute(sql, {"content":content, "id":id})
        db.session.commit()
        return True
            
    return False
