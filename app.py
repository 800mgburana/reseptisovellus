import sqlite3
from flask import *
from werkzeug.security import generate_password_hash
import db
import secrets
import users
import rcps
import cmmnt
import math
from datetime import datetime
import markupsafe
from os import environ

app = Flask(__name__)
app.secret_key = environ["APP_SECRET_KEY"]

def require_login():
    if "user_id" not in session:
        abort(403)

def check_csrf():
    if request.form["csrf_token"] != session ["csrf_token"]:
        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br>")
    return markupsafe.Markup(content)

# pages

@app.route("/")
@app.route("/<int:page>")
def mainpage(page=1):
    page_size = 10
    recipe_count = rcps.recipe_count()
    page_count = math.ceil(recipe_count/page_size)
    page_count = max(page_count, 1)
    now = str(datetime.now())[:19]

    db.execute("INSERT INTO visits (visited_at) VALUES (?)", [now])
    visit_ammount = (db.query("SELECT COUNT(*) FROM visits"))[0][0]
    last_visit = db.query("SELECT visited_at FROM visits ORDER BY visited_at DESC LIMIT 1")[0][0]

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))
    
    recipes = rcps.get_recipes(page, page_size)
    return render_template("mainpage.html", visits = visit_ammount, 
                            date = last_visit, recipes = recipes,
                            page=page, page_count=page_count, count=recipe_count)

@app.route("/recipe/<int:recipe_id>/")
@app.route("/recipe/<int:recipe_id>/<int:page>")
def show_recipe(recipe_id, page=1):
    try:
        recipe = rcps.get_recipe(recipe_id)

    except:
        abort(404)

    if recipe["status"] == 0:
        abort(404)
        
    tags = rcps.get_tags(recipe_id)
    likes = rcps.get_likes(recipe_id)

    page_size = 5
    comment_count = cmmnt.get_comment_count(recipe_id)
    page_count = math.ceil(comment_count/page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/recipe/{recipe_id}/1")
    if page > page_count:
        return redirect(f"/recipe/{recipe_id}/{page_count}")
    
    comments = cmmnt.get_comments(recipe_id, page, page_size)
    
    return render_template("recipe.html", recipe=recipe, tags=tags,
                            likes=likes, comments=comments, page=page, 
                            page_count=page_count, count=comment_count)

@app.route("/user/<int:user_id>")
@app.route("/user/<int:user_id>/<int:page>")
def show_user(user_id, page=1):
    user = users.get_user(user_id)

    if not user:
        abort(404)

    page_size = 15
    recipe_count = users.get_recipe_count(user_id)
    page_count = math.ceil(recipe_count/page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect(f"/user/{user_id}/1")
    if page > page_count:
        return redirect(f"/user/{user_id}/{page_count}")

    recipes = users.get_recipes(user_id, page, page_size)
    return render_template("user.html", user=user, recipes=recipes,
                           page=page, page_count=page_count, recipe_count=recipe_count)

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
        return render_template("register.html", filled={}, next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        if len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]
        next_page = request.form["next_page"]

        if password1 != password2:
            flash("VIRHE: Antamasi salasanat eivät ole samat")
            filled = {"username": username}
            return render_template("register.html", filled=filled, next_page=next_page)

        try:
            password_hash = generate_password_hash(password1)
            db.execute("INSERT INTO users(username, password_hash) VALUES(?, ?)", 
                       (username, password_hash))
            flash("Tunnuksen luominen onnistui, voit nyt kirjautua sisään.")
            return redirect(next_page)

        except sqlite3.IntegrityError:
            flash("VIRHE: Valitsemasi tunnus on jo varattu.")
            filled = {"username": username}
            return render_template("register.html", filled=filled, next_page=next_page)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        global username
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        user_id = users.check_login(username, password)

        if user_id:
            session["user_id"] = user_id
            session["csrf_token"] = secrets.token_hex(16)
            flash("Olet kirjautunut sisään.")
            return redirect(next_page)
        
        else:
            flash("VIRHE: Väärä tunnus tai salasana")
            return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    next_page=request.referrer
    require_login()

    del session["user_id"]
    flash("Olet kirjautunut ulos.")
    return redirect(next_page)

@app.route("/add_image", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("add_image.html", next_page=request.referrer)
    
    if request.method == "POST":
        check_csrf()
        file = request.files["image"]
        if not file.filename.endswith(".jpg"):
            flash("VIRHE: väärä tiedostomuoto")
        
        image = file.read()
        if len(image) > 100*1024:
            flash("VIRHE: liian suuri kuva")
            return redirect("/add_image")
        
        user_id = session["user_id"]
        users.update_image(user_id, image)
        return redirect("/user/" + str(user_id))

# post actions

@app.route("/new", methods = ["GET", "POST"])
def new():
    require_login()

    if request.method == "GET":
        return render_template("new.html", session=session, next_page=request.referrer)
    
    check_csrf()

    if request.method == "POST":
        user_id = session["user_id"]
        title = request.form["title"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        tags = request.form.getlist("tags")

        if len(title) > 50 or len(ingredients) > 500 or len(ingredients) > 1000:
            abort(403)

        try:
            recipe_id = rcps.get_recipe_id()
            rcps.new_post(title, ingredients, instructions, user_id, tags)  
        
        except sqlite3.IntegrityError:
            abort(403)
                                    
        return redirect("/recipe/" + str(recipe_id))

@app.route("/edit/<int:recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    recipe = rcps.get_recipe(recipe_id)
    tags = rcps.get_tags(recipe_id)
    tags = [tag["name"] for tag in tags]

    if not recipe or recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit.html", recipe=recipe, tags=tags,
                               next_page="/recipe/" + str(recipe_id))

    if request.method == "POST":
        check_csrf()
        title = request.form["title"]
        ingredients = request.form["ingredients"]
        instructions = request.form["instructions"]
        tags = request.form.getlist("tags")
        tags = [tag.strip("/") for tag in tags]

        rcps.update_recipe(recipe["id"], title, ingredients, instructions, tags)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/delete/<int:recipe_id>", methods=["GET", "POST"])
def delete_recipe(recipe_id):
    recipe = rcps.get_recipe(recipe_id)

    if not recipe or recipe["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete.html", recipe=recipe)
    
    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            rcps.delete_recipe(recipe_id)
            return redirect("/")
        
        else:
            return redirect("/recipe/" + str(recipe_id))

@app.route("/search")
def search():
    query = request.args.get("query")
    tags = request.args.getlist("tags")
    page = request.args.get("page", default=1, type=int)

    page_size = 10

    if tags and not query:
        flash("Anna hakusana")

    if query and len(query) > 50:
        flash("Liian pitkä hakusana")

    results = rcps.search(query, tags, page, page_size) if query else []
    results_count = rcps.search_count(query, tags)

    page_count = math.ceil(results_count/page_size)
    page_count = max(page_count, 1)

    return render_template("search.html", query=query, tags=tags, 
                           results=results, page=page, page_count=page_count)

@app.route("/like/<int:recipe_id>", methods=["POST"])
def like(recipe_id):
    if "user_id" not in session:
        flash("sinun on kirjauduttava sisään, jotta voit tykätä resepteistä.")

    else:
        rcps.like(recipe_id, session["user_id"])
        
    return redirect("/recipe/" + str(recipe_id))

# comments

@app.route("/comment/<int:recipe_id>", methods=["GET", "POST"])
def comment(recipe_id):
    require_login()
    recipe = rcps.get_recipe(recipe_id)

    if request.method == "GET":
        return render_template("comment.html", recipe=recipe, next_page="/recipe/" + str(recipe_id))

    check_csrf()

    if request.method == "POST":
        content = request.form["comment"]
        user_id = session["user_id"] 

        if len(content) > 300:
            abort(403)

        cmmnt.new_comment(recipe_id, user_id, content)
        return redirect("/recipe/" + str(recipe_id))

@app.route("/edit_comment/<int:comment_id>", methods=["GET", "POST"])   
def edit_comment(comment_id):
    comment = cmmnt.get_comment(comment_id)

    if not comment or comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("edit_comment.html", comment=comment, 
                               next_page="/recipe/" + str(comment["recipe_id"]))
    
    if request.method == "POST":
        check_csrf()
        content = request.form["comment"]
        if len(content) > 300:
            abort(403)

        cmmnt.update_comment(comment["id"], content)
        return redirect("/recipe/" + str(comment["recipe_id"]))

@app.route("/delete_comment/<int:comment_id>", methods=["GET", "POST"])
def delete_comment(comment_id):
    comment = cmmnt.get_comment(comment_id)

    if not comment or comment["user_id"] != session["user_id"]:
        abort(403)

    if request.method == "GET":
        return render_template("delete_comment.html", comment=comment)
    
    if request.method == "POST":
        check_csrf()
        if "continue" in request.form:
            cmmnt.delete_comment(comment_id)

    return redirect("/recipe/" + str(comment["recipe_id"]))

#

@app.route("/mole")
def mole():
    return render_template("mole.html")