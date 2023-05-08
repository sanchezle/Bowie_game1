import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required, lookup, usd

# Configure application
app = Flask(__name__)

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///bowiegame.db")

@app.route("/")
@login_required
def index():
    user_id = session["user_id"]
    user = db.execute("SELECT username FROM users WHERE id = ?", user_id)
    username = user[0]["username"]

    # Replace this with the actual index_data and total_cash calculation
    

    return render_template("index.html")

# Add the additional routes and functions that you have provided
@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    # User reached route via POST (as by submitting a form via POST)
    if request.method == "POST":

        # Ensure username was submitted
        if not request.form.get("username"):
            return apology("must provide username", 403)

        # Ensure password was submitted
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        rows = db.execute("SELECT * FROM users WHERE username = ?", request.form.get("username"))

        # Ensure username exists and password is correct
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Remember which user has logged in
        session["user_id"] = rows[0]["id"]

        # Redirect user to home page
        return redirect("/")

    # User reached route via GET (as by clicking a link or via redirect)
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")
@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        if not username:
            return apology("must provide an username", 403)

        # Check if username already exists
        count = db.execute("SELECT COUNT(*) as count FROM users WHERE username = ?", username)[0]["count"]
        if count > 0:
            return apology("user already exists", 403)

        elif not password:
            return apology("you must provide a password", 403)

        elif not confirmation:
            return apology("you must confirm your password", 403)

        elif password != confirmation:
            return apology("passwords do not match", 403)

        else:
            # Hash the password before storing it
            password_hash = generate_password_hash(password)
            db.execute("INSERT INTO users (username, hash) VALUES(?, ?)", username, password_hash)
            return render_template("success.html")

    return render_template("register.html")


# ... your previous routes ...

# Your provided routes

# ... other routes ...

if __name__ == '__main__':
    app.run()
