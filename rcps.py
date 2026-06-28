from datetime import datetime
import sqlite3
import db

def recipe_count():
    sql = """SELECT COUNT(id) as count
             FROM recipes WHERE status = 1"""
    return db.query(sql)[0]["count"]

def get_recipes(page, page_size):
    sql = """SELECT r.id, r.title, r.date, r.status, u.username, r.user_id
             FROM recipes r, users u
             WHERE r.user_id = u.id AND r.status = 1
             ORDER BY r.date DESC
             LIMIT ? OFFSET ?"""
    limit = page_size
    offset = page_size * (page-1)

    return db.query(sql, [limit, offset])

def get_recipe(recipe_id):
    sql = """SELECT r.id, r.title, r.ingredients, r.instructions,
             r.date, r.status, u.username, r.user_id
             FROM recipes r, users u
             WHERE r.id = ? AND r.user_id = u.id"""

    return db.query(sql, [recipe_id])[0]

def update_recipe(recipe_id, title, ingredients, instructions, tags):
    sql = """UPDATE recipes
             SET title = ?,
                 ingredients = ?,
                 instructions = ?
             WHERE id = ?;"""
    db.execute(sql, [title, ingredients, instructions, recipe_id])

    db.execute("UPDATE recipe_tags SET status = 0 WHERE recipe_id = ?", [recipe_id])
    for tag in tags:
        tag_id = db.query("SELECT id FROM tags WHERE name = ?", [tag])[0][-1]
        sql = """
                UPDATE recipe_tags 
                SET status = 1
                WHERE recipe_id = ?
                AND tag_id = ?
            """
        db.execute(sql, [recipe_id, tag_id])


def delete_recipe(recipe_id):
    sql = """UPDATE recipes
             SET status = 0
             WHERE id = ?"""

    db.execute(sql, [recipe_id])

def search(query, tags, page, page_size):
    sql = """SELECT r.id as recipe_id, r.title,
             r.ingredients, r.date, u.username
             FROM recipes r, users u
             WHERE r.user_id = u.id
             AND r.title LIKE ?"""
    params = ["%" + query + "%"]

    if tags:
        placeholders = ",".join("?" for _ in tags)
        sql += f"""
            AND r.id IN (
                SELECT rt.recipe_id
                FROM recipe_tags rt
                JOIN tags t ON rt.tag_id = t.id
                WHERE rt.status = 1
                AND t.name IN ({placeholders})
                GROUP BY rt.recipe_id
                HAVING COUNT(DISTINCT t.name) = ?
            )
        """
        params.extend(tags)
        params.append(len(tags))

    limit = page_size
    offset = page_size * (page-1)
    sql += """
        ORDER BY r.date DESC
        LIMIT ? OFFSET ?"""
    params.extend([limit, offset])

    return db.query(sql, params)

def search_count(query, tags):
    sql = """
        SELECT COUNT(*)
        FROM recipes r
        WHERE r.title LIKE ?
    """

    params = ["%" + query + "%"]

    if tags:
        placeholders = ",".join("?" for _ in tags)
        sql += f"""
            AND r.id IN (
                SELECT rt.recipe_id
                FROM recipe_tags rt
                JOIN tags t ON rt.tag_id = t.id
                WHERE rt.status = 1
                AND t.name IN ({placeholders})
                GROUP BY rt.recipe_id
                HAVING COUNT(DISTINCT t.name) = ?
            )
        """
        params.extend(tags)
        params.append(len(tags))

    return db.query(sql, params)[0][0]

def new_post(title, ingredients, instructions, user_id, tags):
    now = str(datetime.now())[:19]

    sql = """INSERT INTO recipes(title, ingredients, instructions, date, user_id)
             VALUES(?, ?, ?, ?, ?)"""
    db.execute(sql, [title, ingredients, instructions, now, user_id])

    recipe_id = db.last_insert_id()

    for tag in ["vegetaarinen", "vegaaninen", "laktoositon", "gluteeniton"]:
        tag_id = db.query("SELECT id FROM tags WHERE name = ?", [tag])[0][-1]
        if tag in tags:
            db.execute("INSERT INTO recipe_tags(recipe_id, tag_id) VALUES(?, ?)",
                       [recipe_id, tag_id])
        else:
            db.execute("INSERT INTO recipe_tags(recipe_id, tag_id, status) VALUES(?, ?, 0)",
                       [recipe_id, tag_id])

def get_tags(recipe_id):
    sql = """SELECT t.name
             FROM recipe_tags rt, tags t
             WHERE rt.recipe_id = ?
             AND rt.tag_id = t.id
             AND rt.status = 1"""

    return db.query(sql, [recipe_id])

def like(recipe_id, user_id):
    status = get_like_status(recipe_id, user_id)
    print(status)

    if status == 1:
        db.execute("UPDATE likes SET status = 0 WHERE user_id = ? AND recipe_id = ?",
                    [user_id, recipe_id])

    elif status == 0:
        db.execute("UPDATE likes SET status = 1 WHERE user_id = ? AND recipe_id = ?",
                    [user_id, recipe_id])

    else:
        db.execute("INSERT INTO likes(user_id, recipe_id, status) VALUES(?, ?, 1)",
                    [user_id, recipe_id])

def get_likes(recipe_id):
    sql = """SELECT COUNT(recipe_id) AS count
             FROM likes
             WHERE recipe_id = ?
             AND status = 1"""

    return db.query(sql, [recipe_id])[0]

def get_like_status(recipe_id, user_id):
    sql = """SELECT status AS status
             FROM likes
             WHERE recipe_id = ? AND user_id = ?"""
    result = db.query(sql, [recipe_id, user_id])

    return result[0]["status"] if result else None

def get_recipe_id():
    try:
        previous_id = int(db.query("SELECT MAX(id) AS previous FROM recipes")[0]["previous"])
        return previous_id+1

    except sqlite3.IntegrityError:
        return 1
