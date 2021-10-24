from db import db
import users

def order_by(sort_option):

    order_by = ""

    if sort_option=="1": order_by += " ORDER BY Q.send_time DESC"
    if sort_option=="2": order_by += " ORDER BY Q.send_time ASC"
    if sort_option=="3": order_by += " ORDER BY time DESC NULLS LAST"
    if sort_option=="4": order_by += " ORDER BY time ASC NULLS LAST"

    return order_by

def fetch_all_admins():
    sql = "SELECT username FROM users WHERE users.is_admin=TRUE"
    result = db.session.execute(sql)
    return result.fetchall()

def fetch_all_users(sort_option):
    sql = "SELECT username, creation_time FROM users"
    if sort_option=="1": sql += " ORDER BY users.creation_time DESC"
    if sort_option=="2": sql += " ORDER BY users.creation_time ASC"
    result = db.session.execute(sql)
    return result.fetchall()

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

