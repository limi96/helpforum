from db import db
import users


def vote(voteType, answer_id, answer_points):
    user_id = users.user_id()
    #first check if user is in points
    sql = "SELECT user_id FROM points P WHERE P.user_id = :user_id AND P.answer_id =:answer_id"
    result = db.session.execute(sql, {"user_id":user_id, "answer_id":answer_id})
    check = False

    for i in result: 
        if (i[0] == user_id): 
            check = True
            break
    if check: return False

    #if not in points, count vote
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
    if type =="user_questions":  sql += type       #Need to set ON DELETE CASCADE ON SCHEMA.SQL

    sql += " WHERE id =:id"

    db.session.execute(sql, {"id":id})
    db.session.commit()


def save_answer(answer, question_id):
    user_id = users.user_id()
    points = 0
    if user_id == 0:
        return False
    sql = "INSERT INTO answers (answer_content, answer_points, question_id, user_id, send_time)"\
        " VALUES (:answer_content, :answer_points, :question_id, :user_id, NOW())"
    db.session.execute(sql, {"answer_content":answer,"answer_points":points,"question_id":question_id, "user_id":user_id })
    db.session.commit()

    return True

def fetch_all_answers(question_id, sort_option):
    
    sql = "SELECT U.username, A.question_id, A.answer_content, A.send_time, A.id, A.answer_points FROM answers A, users U "\
        "WHERE A.question_id = :id AND U.id = A.user_id"
        
    if sort_option=="1": sql += " ORDER BY A.send_time DESC"
    if sort_option=="2": sql += " ORDER BY A.send_time ASC"
    if sort_option=="3": sql += " ORDER BY A.answer_points DESC"
    if sort_option=="4": sql += " ORDER BY A.answer_points ASC"

    result = db.session.execute(sql, {"id":question_id})
    return result.fetchall()
    

def post_question(title, question):
    user_id = users.user_id()
    if user_id == 0:
        return False    
    sql = "INSERT INTO user_questions (question_title, question_content, user_id, send_time)"\
         "VALUES (:question_title, :question_content, :user_id, NOW())"
    db.session.execute(sql, {"question_title":title, "question_content":question, "user_id":user_id})
    db.session.commit()
    return True

def fetch_all_questions():
    sql = "SELECT Q.question_title, Q.id, U.username FROM user_questions Q, users U "\
        "WHERE Q.user_id = U.id ORDER BY Q.id"
    result = db.session.execute(sql)
    return result.fetchall()

def fetch_my_questions(user_id):
    sql = "SELECT question_title, id FROM user_questions WHERE user_id = :id"
    result = db.session.execute(sql, {"id":user_id})
    return result.fetchall()

def fetch_question(question_id):
    sql = "SELECT Q.question_title, Q.question_content, U.username, Q.send_time, U.id FROM user_questions Q, users U"\
        " WHERE Q.id = :id AND Q.user_id = U.id"
    id = question_id
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()