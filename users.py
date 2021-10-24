from db import db
from flask import session
from werkzeug.security import check_password_hash, generate_password_hash, secrets

def fetch_users(all, like):
    if all:
        sql = "SELECT username, creation_time FROM users"
        result = db.session.execute(sql)
    else:
        sql ="SELECT username, creation_time FROM users WHERE username ILIKE :like"
        result = db.session.execute(sql, {"like":like})

    user_list = result.fetchall()
    return user_list



def fetch_all_admins():
    sql = "SELECT username FROM users WHERE users.is_admin=TRUE"
    result = db.session.execute(sql)
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
        sql = "INSERT INTO users (username, password) VALUES (:username, :password)"
        db.session.execute(sql, {"username":username, "password":hash_value})
        db.session.commit()
    except:
        return False
    
    return login(username, password)


