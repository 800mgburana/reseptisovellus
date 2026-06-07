import db
from flask import redirect

def get_recipes():
    sql = """SELECT r.id, r.title, r.date, r.status, u.username, r.user_id
             FROM recipes r, users u
             WHERE r.user_id = u.id
             ORDER BY r.id DESC"""
    
    return db.query(sql)

def get_recipe(recipe_id):
    sql = """SELECT r.id, r.title, r.ingredients, r.instructions, 
             r.date, r.status, u.username, r.user_id
             FROM recipes r, users u 
             WHERE r.id = ? AND r.user_id = u.id"""
    
    return db.query(sql, [recipe_id])[0]

def update_recipe(recipe_id, title, ingredients, instructions):
    sql = """UPDATE recipes
             SET title = ?,
                 ingredients = ?,
                 instructions = ?
             WHERE id = ?;"""
    
    db.execute(sql, [title, ingredients, instructions, recipe_id])

def delete_recipe(recipe_id):
    sql = """UPDATE recipes
             SET status = 0
             WHERE id = ?"""
    
    db.execute(sql, [recipe_id])

def search(query):
    sql = """SELECT r.id recipe_id, r.title, r.ingredients,
                    r.date, u.username
             FROM recipes r, users u
             WHERE r.user_id = u.id AND r.title LIKE ?
             ORDER BY r.date DESC"""
    
    return db.query(sql, ["%" + query + "%"])

def new_post(title, ingredients, instructions, user_id, tags):
    sql = """INSERT INTO recipes(title, ingredients, instructions, date, user_id) 
             VALUES(?, ?, ?, datetime('now'), ?)"""
    db.execute(sql, [title, ingredients, instructions, user_id]) 
    
    recipe_id = db.last_insert_id()

    for tag in tags:
        tag_id = db.query("SELECT id FROM tags WHERE name = ?", [tag])[0][-1]
        print("recipe id =", recipe_id, "tag_id =", tag_id)
        db.execute("INSERT INTO recipe_tags(recipe_id, tag_id) VALUES(?, ?)", [recipe_id, tag_id])

def get_tags(recipe_id):
    sql = """SELECT t.name
             FROM recipe_tags rt, tags t
             WHERE rt.recipe_id = ?
             AND rt.tag_id = t.id"""
    
    return db.query(sql, [recipe_id])