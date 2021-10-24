from db import db

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

def user_query(username):
    sql ="SELECT username, creation_time FROM users WHERE username ILIKE :username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchall()