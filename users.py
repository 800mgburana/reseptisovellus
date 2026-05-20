import sqlite3
import db
from werkzeug.security import check_password_hash

def check_login(username, password):
    password_hash = (db.query("SELECT password_hash FROM users WHERE username = (?)", [username]))[0][0]

    return check_password_hash(password_hash, password)