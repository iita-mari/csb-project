import secrets
import sqlite3
import math
import time

from flask import Flask
from flask import abort, flash, make_response, redirect, render_template, request, session, g
import markupsafe

import config
import items
import users

app = Flask(__name__)
app.secret_key = config.secret_key

def require_login():
    if "user_id" not in session:
        abort(403)
# FIXING FLAW 1: CSRF
# def check_csrf():
#    if "csrf_token" not in request.form:
#        abort(403)
#    if request.form["csrf_token"] != session["csrf_token"]:
#        abort(403)

@app.template_filter()
def show_lines(content):
    content = str(markupsafe.escape(content))
    content = content.replace("\n", "<br />")
    return markupsafe.Markup(content)

@app.route("/")
@app.route("/<int:page>")
def index(page=1):
    page_size = 10
    item_count = items.item_count()
    page_count = math.ceil(item_count / page_size)
    page_count = max(page_count, 1)

    if page < 1:
        return redirect("/1")
    if page > page_count:
        return redirect("/" + str(page_count))

    all_items = items.get_items(page, page_size)
    return render_template("index.html", page=page, page_count=page_count, items=all_items)

@app.route("/user/<int:user_id>")
def show_user(user_id):
    user = users.get_user(user_id)
    if not user:
        abort(404)
    user_items = users.get_items(user_id)
    return render_template("show_user.html", user=user, items=user_items)

@app.route("/images", methods=["GET", "POST"])
def add_image():
    require_login()

    if request.method == "GET":
        return render_template("images.html")

    if request.method == "POST":
## FIXING FLAW 1: CSRF
#        check_csrf()

        file = request.files["image"]
        if not file.filename.endswith(".png"):
            flash("ERROR: The uploaded file is not a PNG file")
            return redirect("/images")

        image = file.read()
        if len(image) > 100 * 1024:
            flash("ERROR: The uploaded file is too large")
            return redirect("/images")

        user_id = session["user_id"]
        users.update_image(user_id, image)
        flash("Image uploaded successfully")
        return redirect("/user/" + str(user_id))

@app.route("/image/<int:user_id>")
def show_image(user_id):
    image = users.get_image(user_id)
    if not image:
        abort(404)

    response = make_response(bytes(image))
    response.headers.set("Content-Type", "image/png")
    return response

@app.route("/find_item")
def find_index():
    query = request.args.get("query")
    if query:
        results = items.find_items(query)
    else:
        query = ""
        results = []
    return render_template("find_item.html", query=query, results=results)

@app.route("/item/<int:item_id>")
def show_item(item_id):
    item = items.get_item(item_id)
    if not item:
        abort(404)
    classes = items.get_classes(item_id)
    comments = items.get_comments(item_id)
    return render_template("show_item.html", item=item, classes=classes, comments=comments)

@app.route("/new_item")
def new_item():
    require_login()
    classes = items.get_all_classes()
    return render_template("new_item.html", classes=classes)

@app.route("/create_item", methods=["POST"])
def create_item():
    require_login()
# FIXING FLAW 1: CSRF
#    check_csrf()

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    difficulty_level = request.form["difficulty_level"]
    rating = request.form["rating"]
    user_id = session["user_id"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.add_item(title, difficulty_level, rating, user_id, classes)

    return redirect("/")

@app.route("/create_comment", methods=["POST"])
def create_comment():
    require_login()
# FIXING FLAW 1: CSRF
#    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    comment_text = request.form["comment_text"]
    if not comment_text:
        flash("ERROR: The comment cannot be empty")
        return redirect("/item/" + str(item_id))
    if not item:
        flash("ERROR: Invalid item")
        return redirect("/")
    if len(comment_text) > 5000:
        flash("ERROR: The comment is too long (over 5000 characters)")
        return redirect("/item/" + str(item_id))
    user_id = session["user_id"]

    items.add_comment(item_id, user_id, comment_text)

    return redirect("/item/" + str(item_id))

@app.route("/edit_item/<int:item_id>")
def edit_item(item_id):
    require_login()
    item = items.get_item(item_id)
    if not item:
        abort(404)
    # FLAW 3: BROKEN ACCESS CONTROL
# FIXING FLAW 3: BROKEN ACCESS CONTROL
#    if item["user_id"] != session["user_id"]:
#        abort(403)

    all_classes = items.get_all_classes()
    classes = {}
    for my_class in all_classes:
        classes[my_class] = ""
    for entry in items.get_classes(item_id):
        classes[entry["title"]] = entry["value"]

    return render_template("edit_item.html", item=item, classes=classes,
    all_classes=all_classes)

@app.route("/update_item", methods=["POST"])
def update_item():
    require_login()
# FIXING FLAW 1: CSRF
#    check_csrf()

    item_id = request.form["item_id"]
    item = items.get_item(item_id)
    if not item:
        abort(404)
    # FLAW 3: BROKEN ACCESS CONTROL
# FIXING FLAW 3: BROKEN ACCESS CONTROL
#    if item["user_id"] != session["user_id"]:
#        abort(403)

    title = request.form["title"]
    if not title or len(title) > 50:
        abort(403)
    difficulty_level = request.form["difficulty_level"]
    rating = request.form["rating"]

    all_classes = items.get_all_classes()

    classes = []
    for entry in request.form.getlist("classes"):
        if entry:
            class_title, class_value = entry.split(":")
            if class_title not in all_classes:
                abort(403)
            if class_value not in all_classes[class_title]:
                abort(403)
            classes.append((class_title, class_value))

    items.update_item(item_id, title, difficulty_level, rating, classes)

    return redirect("/item/" + str(item_id))

@app.route("/remove_item/<int:item_id>", methods=["GET", "POST"])
def remove_item(item_id):
    require_login()

    item = items.get_item(item_id)
    if not item:
        abort(404)
    # FLAW 3: BROKEN ACCESS CONTROL
# FIXING FLAW 3: BROKEN ACCESS CONTROL
#    if item["user_id"] != session["user_id"]:
#        abort(403)

    if request.method == "GET":
        return render_template("remove_item.html", item=item)

    if request.method == "POST":
# FIXING FLAW 1: CSRF
#        check_csrf()
        if "remove" in request.form:
            items.remove_item(item_id)
            return redirect("/")
        else:
            return redirect("/item/" + str(item_id))

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "GET":
        return render_template("register.html", filled={})

    if request.method == "POST":
        username = request.form["username"]
        if not username or len(username) > 16:
            abort(403)
        password1 = request.form["password1"]
        password2 = request.form["password2"]

        # FLAW 5: IDENTIFICATION AND AUTHENTICATION FAILURES
        if not password1:
            abort(403)
# FIXING FLAW 5: IDENTIFICATION AND AUTHENTICATION FAILURES
#        if not password1 or len(password1) < 12:
#            abort(403)
        if password1 != password2:
            flash("ERROR: The passwords are not the same")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

        try:
            users.create_user(username, password1)
        except sqlite3.IntegrityError:
            flash("ERROR: Username is already taken")
            filled = {"username": username}
            return render_template("register.html", filled=filled)

    flash("Account created. You can now log in.")
    return redirect("/")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html", next_page=request.referrer)

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        next_page = request.form["next_page"]

        user_id = users.check_login(username, password)
        if user_id:
            session["user_id"] = user_id
            session["username"] = username
            session["csrf_token"] = secrets.token_hex(16)
            return redirect(next_page)
        else:
            flash("ERROR: Invalid username or password")
            return render_template("login.html", next_page=next_page)

@app.route("/logout")
def logout():
    if "user_id" in session:
        del session["user_id"]
        del session["username"]
    return redirect("/")

@app.before_request
def before_request():
    g.start_time = time.time()

@app.after_request
def after_request(response):
    elapsed_time = round(time.time() - g.start_time, 3)
    print("elapsed time:", elapsed_time, "s")
    return response