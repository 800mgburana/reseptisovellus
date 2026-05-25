import db

def get_recipes():
    sql = """SELECT id, title, date
             FROM recipes
             ORDER BY id DESC"""
    return db.query(sql)

def get_recipe(thread_id):
    sql = """SELECT id, title, ingredients, instructions 
             FROM recipes 
             WHERE id = ?"""
    return db.query(sql, [thread_id])[0]