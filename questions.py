from db import db
import users



def post(title, question):
    user_id = users.user_id()
    if user_id == 0:
        print("I'm here")
        return False    
    sql = "INSERT INTO user_questions (question_title, question_content, user_id, send_time)"\
         "VALUES (:question_title, :question_content, :user_id, NOW())"
    db.session.execute(sql, {"question_title":title, "question_content":question, "user_id":user_id})
    db.session.commit()
    return True

def fetchAllQuestions():
    sql = "SELECT Q.question_title, U.username FROM user_questions Q, users U "\
        "WHERE Q.user_id = U.id ORDER BY Q.id"

        #SELECT Q.question_title, U.username FROM user_questions Q, users U WHERE Q.id = U.id ORDER BY Q.id
    result = db.session.execute(sql)
    list = result.fetchall()
    return list

def fetchMyQuestions(user_id):
    sql = "SELECT question_title FROM user_questions WHERE user_id = :id"
    result = db.session.execute(sql, {"id":user_id})
    list = result.fetchall()

    return list