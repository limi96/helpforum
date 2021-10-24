from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash, secrets


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

def user_query(username):
    sql ="SELECT username, creation_time FROM users WHERE username ILIKE :username"
    result = db.session.execute(sql, {"username":username})
    return result.fetchall()



def login(username, password):

    sql = "SELECT id, password FROM users WHERE username=:username"
    result = db.session.execute(sql, {"username":username})
    user = result.fetchone()
    if not user:
        return False
    else:
        hash_value = user.password
        if check_password_hash(hash_value, password):
            session["user_id"]  = user.id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return True
        else:
            return False
            
def user_id():
    return session.get("user_id", 0)

def logout():
    del session["user_id"]

def register(username, password):
    hash_value = generate_password_hash(password)

    try: 
        sql = "INSERT INTO users (username, password,creation_time) VALUES (:username, :password,NOW())"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    
    return login(username, password)


