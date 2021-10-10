from db import db
import users


def index_query():
    sql = "SELECT Q.question_title, Q.id, U.username, A.send_time FROM users U, user_questions Q, answers A " \
    "WHERE A.question_id = Q.id AND Q.user_id = U.id ORDER BY A.send_time DESC LIMIT 5"
    
    result = db.session.execute(sql)
    return result.fetchall()


def question_query(query):
    
    sql ="SELECT id, question_title, question_content FROM user_questions WHERE "\
         "question_title LIKE :like OR question_content LIKE :like"
    result = db.session.execute(sql, {"like":query})

    return result.fetchall()

def answer_query(query):
    
    sql ="SELECT id, answer_content FROM answers WHERE "\
         "answer_content LIKE :like"
    result = db.session.execute(sql, {"like":query})

    return result.fetchall()


def vote(voteType, answer_id, answer_points):
    user_id = users.user_id()
    #First check if user is in points
    sql = "SELECT user_id FROM points P WHERE P.user_id = :user_id AND P.answer_id =:answer_id"
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
    sql = "SELECT Q.question_title, Q.question_content, Q.send_time, Q.edited_time, U.is_admin, U.username, U.id "\
         "FROM user_questions Q, users U"\
        " WHERE Q.id = :id AND Q.user_id = U.id"

    result = db.session.execute(sql, {"id":question_id})
    return result.fetchone()

def fetch_all_answers(question_id, sort_option):
    
    sql = "SELECT U.username, A.question_id, A.answer_content, A.send_time, A.id, A.answer_points, A.edited_time FROM answers A, users U "\
        "WHERE A.question_id = :id AND U.id = A.user_id"
        
    if sort_option=="1": sql += " ORDER BY A.send_time DESC"
    if sort_option=="2": sql += " ORDER BY A.send_time ASC"
    if sort_option=="3": sql += " ORDER BY A.answer_points DESC"
    if sort_option=="4": sql += " ORDER BY A.answer_points ASC"

    result = db.session.execute(sql, {"id":question_id})
    return result.fetchall()



def fetch_answer(answer_id):
    sql = "SELECT answer_content FROM answers WHERE id=:id"

    result = db.session.execute(sql, {"id":answer_id})
    return result.fetchone()


def commit_edit(type, id, title, content):
    
    if type=="question":
        sql = "UPDATE user_questions SET question_content=:content, question_title=:title, edited_time=NOW() WHERE id=:id"
        db.session.execute(sql, {"title":title, "content":content, "id":id})
        db.session.commit()
        return True
        
    if type=="answer":
        sql = "UPDATE answers SET answer_content=:content, edited_time=NOW() WHERE id=:id"
        db.session.execute(sql, {"content":content, "id":id})
        db.session.commit()
        return True
            
    return False
