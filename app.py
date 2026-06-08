import sqlite3
from flask import *
from werkzeug.security import generate_password_hash
import db
import secrets
import users
import rcps
import cmmnt

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)

def require_login():
    if "user_id" not in session:
        abort(403)

# pages

@app.route("/")
def mainapge():
    db.execute("INSERT INTO visits (visited_at) VALUES (datetime('now'))")

    visit_ammount = (db.query("SELECT COUNT(*) FROM visits"))[0][0]
    last_visit = db.query("SELECT visited_at FROM visits ORDER BY visited_at DESC LIMIT 1")[0][0]

    recipes = rcps.get_recipes()
    return render_template("mainpage.html", visits = visit_ammount, 
                            date = last_visit, recipes = recipes)

@app.route("/recipe/<int:recipe_id>")
def show_recipe(recipe_id):
    recipe = rcps.get_recipe(recipe_id)
    tags = rcps.get_tags(recipe_id)
    likes = rcps.get_likes(recipe_id)
    comments = cmmnt.get_comments(recipe_id)
    like_status = False
    if "user_id" in session:
        like_status = rcps.get_like_status(recipe_id, session["user_id"])
    
    return render_template("recipe.html", recipe=recipe, tags=tags,
                           likes=likes, comments=comments, like_status=like_status)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)

    if not user:
        abort(404)

    recipes = users.get_recipes(user_id)

    return render_template("user.html", user=user, recipes=recipes)

@app.route("/user/image/<int:user_id>")
def show_user_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/jpeg")
    return response

# user actions

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        if password1 != password2:
            flash("VIRHE: Antamasi salasanat eivät ole samat")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        try:
            password_hash = generate_password_hash(password1)
            db.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", 
                       (username, password_hash))
            flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään")
            return redirect("/")

        except sqlite3.IntegrityError:
            flash("VIRHE: Valitsemasi tunnus on jo varattu")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

@app.route("/login", methods=["GET", "POST"]) # add next page?
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        global username
        username = request.form["username"]
        password = request.form["password"]
        next_page = "/"

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)
        
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    require_login()

    del session["user_id"]
    flash("Olet kirjautunut ulos.")
    return redirect("/")

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_image.html")
    
    if request.method == "POST":
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            return "VIRHE: väärä tiedostomuoto"
        
        image = file.read()
        if len(image) > 100*1024:
            return "VIRHE: liian suuri kuva"
        
        user_id = session["user_id"]
        users.update_image(user_id, image)
        return redirect("/user/" + str(user_id))

# post actions

@app.route("/new", methods = ["GET", "POST"])
def new():
    require_login()

    if request.method == "GET":
        return render_template("new.html")
    
    if request.method == "POST":
        user_id = session["user_id"]
        title = request.form["title"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        tags = request.form.getlist("tags")

        rcps.new_post(title, ingredients, instructions, user_id, tags)       
        recipe_id = str(db.last_insert_id())                                    
        return redirect("/recipe/" + recipe_id)

@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = rcps.get_recipe(recipe_id)

    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", recipe=recipe)

    if request.method == "POST":
        title = request.form["title"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]

        rcps.update_recipe(recipe["id"], title, ingredients, instructions)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/delete/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    recipe = rcps.get_recipe(recipe_id)

    if recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete.html", recipe=recipe)
    
    if request.method == "POST":
        if "continue" in request.form:
            rcps.delete_recipe(recipe_id)
            return redirect("/")
        
        else:
            return redirect("/recipe/" + str(recipe_id))

@app.route("/search")
def search():
    query = request.args.get("query")
    tags = request.args.getlist("tags")
    results = rcps.search(query, tags) if query else []

    if tags and not query:
        flash("Anna hakusana")

    if query and len(query) > 50:
        flash("Liian pitkä hakusana")

    return render_template("search.html", query=query, tags=tags, results=results)

@app.route("/like/<int:recipe_id>", methods=["POST"])
def like(recipe_id):
    try:
        rcps.like(recipe_id, session["user_id"])

    except:
        flash("sinun on kirjauduttava sisään, jotta voit tykätä resepteistä.")
    return redirect("/recipe/" + str(recipe_id))

# comments

@app.route("/comment/<int:recipe_id>", methods=["GET", "POST"])
def comment(recipe_id):
    recipe = rcps.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("comment.html", recipe=recipe)

    if request.method == "POST":
        content = request.form["comment"]
        user_id = session["user_id"] 

        cmmnt.new_comment(recipe_id, user_id, content)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])   
def edit_comment(comment_id):
    comment = cmmnt.get_comment(comment_id)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_comment.html", comment=comment)
    
    if request.method == "POST":
        content = request.form["comment"]
        cmmnt.update_comment(comment["id"], content)
        return redirect("/recipe/" + str(comment["recipe_id"]))

@app.route("/delete_comment/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    comment = cmmnt.get_comment(comment_id)

    if comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_comment.html", comment=comment)
    
    if request.method == "POST":
        if "continue" in request.form:
            cmmnt.delete_comment(comment_id)

    return redirect("/recipe/" + str(comment["recipe_id"]))

#

@app.route("/mole")
def mole():
    return render_template("mole.html")