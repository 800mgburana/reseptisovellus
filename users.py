from werkzeug.security import check_password_hash
import db

def check_login(username, password):
    sql = "SELECT id, password_hash FROM users WHERE username = ?"
    result = db.query(sql, [username])

    if len(result) == 1:
        user_id, password_hash = result[0]
        if check_password_hash(password_hash, password):
            return user_id

    return None

def get_user(user_id):
    sql = """SELECT id, username, image IS NOT NULL has_image
             FROM users
             WHERE id = ?"""

    result = db.query(sql, [user_id])
    return result[0] if result else None

def get_recipes(user_id, page, page_size):
    sql = """SELECT id, title, date
             FROM recipes
             WHERE user_id = ?
             AND status = 1
             ORDER BY date DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page-1)

    return db.query(sql, [user_id, limit, offset])

def get_recipe_count(user_id):
    sql = """SELECT COUNT(id) as count
             FROM recipes 
             WHERE status = 1
             AND user_id = ?"""
    return db.query(sql, [user_id])[0]["count"]

def update_image(user_id, image):
    sql = "UPDATE users SET image = ? WHERE id = ?"
    db.execute(sql, [image, user_id])

def get_image(user_id):
    sql = "SELECT image FROM users WHERE id = ?"
    result = db.query(sql, [user_id])
    return result[0][0] if result else None
