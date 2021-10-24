from db import db
import users

def order_by(sort_option):

    order_by = ""

    if sort_option=="1": order_by += " ORDER BY Q.send_time DESC"
    if sort_option=="2": order_by += " ORDER BY Q.send_time ASC"
    if sort_option=="3": order_by += " ORDER BY time DESC NULLS LAST"
    if sort_option=="4": order_by += " ORDER BY time ASC NULLS LAST"

    return order_by


def fetch_my_questions(username,sort_option):

    sql =   "SELECT Q.question_title, Q.id, Q.send_time, MAX(A.send_time) as time " \
            "FROM user_questions Q " \
            "LEFT JOIN answers A " \
            "ON A.question_id = Q.id " \
            "LEFT JOIN users U " \
            "ON Q.user_id = U.id " \
            "WHERE U.username ILIKE :username "\
            "GROUP BY Q.id, U.username "            
    
    sql += order_by(sort_option)

    result = db.session.execute(sql, {"username":username})
    return result.fetchall()

def fetch_recent_questions(username):
    
    sql =   "SELECT Q.question_title, Q.id, Q.send_time, MAX(A.send_time) as time " \
            "FROM user_questions Q " \
            "LEFT JOIN answers A " \
            "ON A.question_id = Q.id " \
            "LEFT JOIN users U " \
            "ON Q.user_id = U.id " \
            "WHERE U.username ILIKE :username "\
            "GROUP BY Q.id, U.username " \
            "ORDER BY send_time DESC LIMIT 5" 

    result = db.session.execute(sql, {"username":username})
    return result.fetchall()

def fetch_all_questions(sort_option):

    sql =   "SELECT Q.question_title, Q.id, Q.send_time, MAX(A.send_time) as time " \
            "FROM user_questions Q " \
            "LEFT JOIN answers A " \
            "ON A.question_id = Q.id " \
            "GROUP BY Q.id"

    sql += order_by(sort_option)

    result = db.session.execute(sql)
    return result.fetchall()


def fetch_solved_questions(sort_option):

    sql =   "SELECT Q.question_title, Q.id, Q.send_time, MAX(A.send_time) as time " \
            "FROM users U, user_questions Q, answers A, solved S " \
            "WHERE A.question_id = Q.id AND Q.user_id = U.id " \
            "AND Q.user_id = U.id AND S.question_id=Q.id "\
            "GROUP BY Q.id, U.username "

    sql += order_by(sort_option)

    result = db.session.execute(sql)
    return result.fetchall()


def fetch_recent_answers(username):
    sql =   "SELECT A.question_id, A.id, U.username, A.answer_content, Q.question_title, A.send_time "\
            "FROM answers A, user_questions Q, users U " \
            "WHERE U.username ILIKE :username " \
            "AND U.id = A.user_id " \
            "AND A.question_id = Q.id " \
            "ORDER BY A.send_time DESC LIMIT 5"
    
    result = db.session.execute(sql, {"username":username})
    return result.fetchall()

def fetch_my_answers(username,sort_option):

    sql =   "SELECT A.question_id, A.id, U.username, A.answer_content, Q.question_title, A.answer_points, A.send_time "\
            "FROM answers A, user_questions Q, users U " \
            "WHERE U.username ILIKE :username "\
            "AND U.id = A.user_id " \
            "AND A.question_id = Q.id"

    if sort_option=="1": sql += " ORDER BY A.send_time DESC"
    if sort_option=="2": sql += " ORDER BY A.send_time ASC"
    if sort_option=="3": sql += " ORDER BY A.answer_points DESC"
    if sort_option=="4": sql += " ORDER BY A.answer_points ASC"

    result = db.session.execute(sql, {"username":username})
    return result.fetchall()


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




def fetch_solved_answer(question_id):

    sql =   "SELECT S.answer_id, U.username, A.question_id, A.answer_content, A.send_time, A.id, A.answer_points, A.edited_time " \
            "FROM answers A, users U, solved S "\
            "WHERE A.question_id = :id AND U.id = A.user_id AND S.answer_id = A.id"

    result = db.session.execute(sql,{"id":question_id})
    return result.fetchall()




def fetch_question(question_id):
    sql =   "SELECT Q.question_title, Q.question_content, Q.send_time, Q.edited_time, U.is_admin, U.username, U.id "\
            "FROM user_questions Q, users U "\
            "WHERE Q.id = :id AND Q.user_id = U.id"

    result = db.session.execute(sql, {"id":question_id})
    return result.fetchone()

def fetch_all_answers(question_id, sort_option):
    
    sql =   "SELECT U.username, A.question_id, A.answer_content, A.send_time, A.id, A.answer_points, A.edited_time " \
            "FROM answers A, users U "\
            "WHERE A.question_id = :id AND U.id = A.user_id"

    if sort_option=="1": sql += " ORDER BY A.send_time DESC"
    if sort_option=="2": sql += " ORDER BY A.send_time ASC"
    if sort_option=="3": sql += " ORDER BY A.answer_points DESC"
    if sort_option=="4": sql += " ORDER BY A.answer_points ASC"

    result = db.session.execute(sql, {"id":question_id})

    return result.fetchall()

def fetch_answer(answer_id):
    sql =   "SELECT answer_content FROM answers WHERE id=:id"
    result = db.session.execute(sql, {"id":answer_id})
    return result.fetchone()


def index_query():
    sql =   "SELECT Q.question_title, Q.id, U.username, MAX(A.send_time) as time " \
            "FROM users U, user_questions Q, answers A " \
            "WHERE A.question_id = Q.id AND Q.user_id = U.id " \
            "GROUP BY Q.id, U.username " \
            "ORDER BY time DESC LIMIT 5"
    
    result = db.session.execute(sql)

    return result.fetchall()

def question_query(query, posted_by):
    if posted_by == "":

        sql =   "SELECT Q.question_title, Q.id, Q.send_time, MAX(A.send_time) as time " \
                "FROM user_questions Q " \
                "LEFT JOIN answers A " \
                "ON A.question_id = Q.id " \
                "WHERE question_title ILIKE :like OR question_content ILIKE :like " \
                "GROUP BY Q.id" \

        result = db.session.execute(sql, {"like":query})
        return result.fetchall()

    else:

        sql =   "SELECT Q.question_title, Q.id, Q.send_time, MAX(A.send_time) as time " \
                "FROM user_questions Q " \
                "LEFT JOIN answers A " \
                "ON A.question_id = Q.id " \
                "LEFT JOIN users U " \
                "ON Q.user_id = U.id " \
                "WHERE U.username ILIKE :posted_by " \
                "AND (question_title ILIKE :like OR question_content ILIKE :like) "\
                "GROUP BY Q.id, U.username " \
                    
        result = db.session.execute(sql, {"like":query, "posted_by":posted_by})
        return result.fetchall()
        

def answer_query(query, posted_by):
    if posted_by == "":

        sql =   "SELECT A.question_id, A.id, A.answer_content, Q.question_title, A.answer_points, A.send_time "\
                "FROM answers A, user_questions Q "\
                "WHERE answer_content ILIKE :like "\
                "AND A.question_id = Q.id"
        
        result = db.session.execute(sql, {"like":query})
        return result.fetchall()

    else: 

        sql =   "SELECT A.question_id, A.id, U.username, A.answer_content, Q.question_title, A.answer_points, A.send_time "\
                "FROM answers A, user_questions Q, users U " \
                "WHERE U.username ILIKE :posted_by " \
                "AND answer_content ILIKE :like " \
                "AND U.id = A.user_id " \
                "AND A.question_id = Q.id"
    
        result = db.session.execute(sql, {"like":query, "posted_by":posted_by})
        return result.fetchall()


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
