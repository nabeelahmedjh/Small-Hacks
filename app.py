from crypt import methods
import os
from click import pass_obj

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from datetime import datetime

from helpers import apology, login_required, lookup, usd, validatePass, generatePass

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True


# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
# database
db = SQL("sqlite:///smallhacks.db")


@app.route("/")
@login_required
def homepage():
    return redirect("/index")


@app.route("/index")
@login_required
def index():

    communityPosts = db.execute("SELECT * FROM posts ORDER BY post_id DESC")

    return render_template("index.html", communityPosts=communityPosts)


@app.route("/login", methods=["GET", "POST"])
def login():

    session.clear()
    # TODO: log user in

    if request.method == "GET":
        return render_template("login.html")

    else:

        # checking for test cases
        if not request.form.get("username") or not request.form.get("password"):
            return apology("MUST PROVIDE USERNAME AND PASSWORD")

        username = request.form.get("username")
        password = request.form.get("password")

        userInfo = db.execute(
            "SELECT * FROM users WHERE name = ?", username)

        # checking the username and password are right or wrong
        if len(userInfo) == 0 or check_password_hash(userInfo[0]["hash"], password) == 0:
            return apology("USERNAME OR PASSWORD IS INCORRECT")

        session["user_id"] = userInfo[0]["id"]
        return redirect("/index")


@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":

        # confirming all fields are filled
        if not request.form.get("username"):
            return apology("MUST PROVIDE USERNAME")

        name = request.form.get("username")

        if not request.form.get("password"):
            return apology("MUST PROVIDE password")

        if not request.form.get("confirmation"):
            return apology("MUST PROVIDE CONFIRM PASSWORD")

        password = request.form.get("password")

        if validatePass(password) == False:
            return apology("YOUR PASSWORD DOESN'T SATISFY THE REQUIRMENTS, YOU CAN GENERATE PASSWORD BY CLICKING GENERATE A PASSWORD ON NAVBAR")

        # checking if password and cofirm password matches
        if password != request.form.get("confirmation"):
            return apology("PASSWORD DOESNT MATCH PASSOWRD AND CONFIRM PASSWORD FIELDS")

        # Checking if the username already exist or not
        userCheck = db.execute("SELECT * FROM users WHERE name = ?", name)

        if len(userCheck) != 0:
            return apology("USER ALREADY EXIST")

        db.execute("INSERT INTO users (name, hash) VALUES (?, ?)",
                   name, generate_password_hash(password))

        userData = db.execute("SELECT * FROM users WHERE name = ?", name)

        return redirect("/index")

    else:
        return render_template("register.html")


@app.route("/publishpost", methods=["GET", "POST"])
@login_required
def communityPost():

    if request.method == "POST":

        post = request.form.get("communityPost")

        # returning error if user writes nothing
        if not post:
            return apology("Must require something to write")

        userInfo = db.execute(
            "SELECT * FROM users WHERE id = ?", session["user_id"])

        db.execute("INSERT INTO posts (user_id, username, post_data, datetime) VALUES (?, ?, ?, ?)",
                   session["user_id"], userInfo[0]["name"], post, datetime.now())

        return redirect("/index")

    else:
        return render_template("publishpost.html")


@app.route("/logout", methods=["GET"])
@login_required
def logout():

    # clearing the session
    session.clear()

    # redirecting to index
    return redirect("/index")


@app.route("/generatepass", methods=["GET", "POST"])
def generatePassword():

    if request.method == "POST":

        password = generatePass()
        return render_template("generatedpass.html", password=password)

    else:
        return render_template("generatepass.html")


@app.route("/validatepass", methods=["GET", "POST"])
def validatePassword():

    if request.method == "POST":

        password = request.form.get("password")
        if not password:
            return apology("Must provide a password")

        if validatePass(password) == False:
            return apology("YOUR PASSWORD IS NOT SATISFYING THE GIVEN REQUIRMENTS")

        return render_template("validatedpass.html")

    else:
        return render_template("validatepass.html")


@app.route("/yourposts")
@login_required
def yourPosts():
    yourPosts = db.execute(
        "SELECT * FROM POSTS WHERE user_id = ? ORDER BY datetime DESC", session["user_id"])

    if len(yourPosts) == 0:
        return apology("YOU HAV'NT WROTE ANY POST YET CLICK ON PUBLISH A POST TO PUBLISH A POST")

    return render_template("yourposts.html", yourPosts=yourPosts)


if __name__ == "__main__":
    app.run(debug=True)
