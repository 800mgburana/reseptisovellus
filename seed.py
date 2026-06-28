import random
import sqlite3
import time

print("started")
start = time.time()

db = sqlite3.connect("database.db")

db.execute("DELETE FROM users")
db.execute("DELETE FROM recipes")
db.execute("DELETE FROM comments")

user_count = 1000
recipe_count = 10**5
comments_count = 10**6

for i in range(1, user_count+1):
    db.execute("INSERT INTO users (username) VALUES (?)", ["User" + str(i)])

for i in range(1, recipe_count+1):
    user_id = random.randint(1, user_count)
    sql = """
            INSERT INTO recipes 
            (title, ingredients, instructions, user_id) 
            VALUES 
            (?, 'Ingredients', 'Instructions', ?)
            """
    db.execute(sql, ["Recipe" + str(i), user_id])
    
    tag_ammount = random.randint(0, 5)
    if tag_ammount != 0:
        for tag in range(1, tag_ammount+1):
            sql = """
                    INSERT INTO recipe_tags
                    (recipe_id, tag_id)
                    VALUES
                    (?, ?)"""
            
            db.execute(sql, [i, tag])

for i in range(1, comments_count+1):
    user_id = random.randint(1, user_count)
    recipe_id = random.randint(1, recipe_count)
    db.execute("INSERT INTO comments (user_id, recipe_id, content) VALUES (?,?, ?)", [user_id, recipe_id, "Message" + str(i)])

db.commit()
db.close()

print("ended. took:", time.time()-start, "s")