from db import db
import users


def vote(UPvote, answer_id, answer_points):
    user_id = users.user_id()

    #first check if user is in points
    sql = "SELECT user_id FROM points P WHERE P.user_id = :user_id AND P.answer_id =:answer_id"
    result = db.session.execute(sql, {"user_id":user_id, "answer_id":answer_id})
    check = False
    for i in result: 
        print(i)
        if (i[0] == user_id): 
            check = True
            break
    if check: return False

    #if not in points, count vote
    insert_points = int(answer_points)+1 if (UPvote) else int(answer_points)-1

    sql = "INSERT INTO points (result, answer_id, user_id) VALUES (:result, :answer_id, :user_id)" 
    db.session.execute(sql, {"result":insert_points, "answer_id":answer_id, "user_id":user_id })
    db.session.commit()

    sql = "UPDATE answers SET answer_points=:insert_points WHERE id =:answer_id"
    db.session.execute(sql, {"insert_points":insert_points, "answer_id":answer_id})
    db.session.commit()        
    return True

def fetchVotes():

    return 0

def postAnswer(answer, question_id):
    user_id = users.user_id()
    points = 0
    if user_id == 0:
        return False
    sql = "INSERT INTO answers (answer_content, answer_points, question_id, user_id, send_time)"\
        " VALUES (:answer_content, :answer_points, :question_id, :user_id, NOW())"
    db.session.execute(sql, {"answer_content":answer,"answer_points":points,"question_id":question_id, "user_id":user_id })
    db.session.commit()

    return True

def fetchAllAnswers(question_id):
    #sql = "SELECT Q.id, A.answer_content, U.username, A.send_time FROM answers A, users U, user_questions Q"\
    #    " WHERE A.question_id = Q.id AND A.user_id = U.id"
    
    #sql = "SELECT A.question_id, A.answer_content, A.send_time FROM answers A INNER JOIN user_questions Q"\
    #    " ON A.question_id = Q.id"
    
    sql = "SELECT U.username, A.question_id, A.answer_content, A.send_time, A.id, A.answer_points FROM answers A, users U "\
        "WHERE A.question_id = :id AND U.id = A.user_id ORDER BY A.send_time"

    #ORDER BY A.answer_points
    #SELECT A.answer_points

    result = db.session.execute(sql, {"id":question_id})
    return result.fetchall()
    
def postQuestion(title, question):
    user_id = users.user_id()
    if user_id == 0:
        return False    
    sql = "INSERT INTO user_questions (question_title, question_content, user_id, send_time)"\
         "VALUES (:question_title, :question_content, :user_id, NOW())"
    db.session.execute(sql, {"question_title":title, "question_content":question, "user_id":user_id})
    db.session.commit()
    return True

def fetchAllQuestions():
    sql = "SELECT Q.question_title, Q.id, U.username FROM user_questions Q, users U "\
        "WHERE Q.user_id = U.id ORDER BY Q.id"
    result = db.session.execute(sql)
    return result.fetchall()

def fetchMyQuestions(user_id):
    sql = "SELECT question_title, id FROM user_questions WHERE user_id = :id"
    result = db.session.execute(sql, {"id":user_id})
    return result.fetchall()

def fetchQuestion(question_id):
    sql = "SELECT Q.question_title, Q.question_content, U.username, Q.send_time FROM user_questions Q, users U"\
        " WHERE Q.id = :id AND Q.user_id = U.id"
    id = question_id
    result = db.session.execute(sql, {"id":id})
    return result.fetchone()