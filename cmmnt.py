import db

def new_comment(recipe_id, user_id, content):
    sql = """INSERT INTO comments(content, sent_at, user_id, recipe_id)
             VALUES(?, datetime('now'), ?, ?)"""
    db.execute(sql, [content, user_id, recipe_id])

def update_comment(id, content):
    sql = """UPDATE comments
             SET content = ?
             WHERE id = ?;"""
    db.execute(sql, [content, id])

def delete_comment(id):
    sql = """UPDATE comments
             SET status = 0
             WHERE id = ?"""
    db.execute(sql, [id])

def get_comments(recipe_id, page, page_size):
    sql = """SELECT c.id, c.content, c.sent_at, c.user_id, u.username
             FROM comments c, users u
             WHERE c.user_id = u.id AND c.recipe_id = ? AND c.status = 1
             ORDER BY c.id DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page-1)
    
    return db.query(sql, [recipe_id, limit, offset])

def get_comment(comment_id):
    sql = """SELECT c.id, c.content, c.recipe_id, c.user_id
             FROM comments c, users u
             WHERE c.id = ? AND c.user_id = u.id"""
    
    return db.query(sql, [comment_id])[0]

def get_comment_count(recipe_id):
    sql = """SELECT COUNT(id) as count
             FROM comments 
             WHERE status = 1
             AND recipe_id = ?"""
    return db.query(sql, [recipe_id])[0]["count"]