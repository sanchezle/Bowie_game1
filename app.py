import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response, jsonify
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from helpers import apology, login_required
from flask_socketio import SocketIO, emit
from datetime import datetime

# Configure application
#q: are all off the routes underneaty properly indented?
#a: yes, they are properly indented

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "bowiegame.db")
db = SQL(f"sqlite:///{db_path}")

DATABASE="bowiegame.db"
# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Configure CS50 Library to use SQLite database
socketio = SocketIO(app)


# Function to connect to the SQLite database
def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

@app.route('/users')
def get_users():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    # Do something with the fetched data, like return it as JSON or render a template



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

from datetime import datetime

# Your existing code

@app.route('/update_score', methods=["GET", "POST"])
def update_score():
    data = request.get_json()
    score = data.get('score', None)

    if score is not None:
        # Get the current timestamp
        timestamp = datetime.now()

        # Insert the record into the database, including the timestamp
        db.execute("INSERT INTO scores (user_id, score, timestamp) VALUES(?, ?, ?)", session["user_id"], score, timestamp)

        # Other existing code

    else:
        return jsonify({'status': 'error', 'message': 'Score not received'}), 400

# Your other routes and code


# q: when the '/updatescore' route is going to be calle?
# a
# just renders the templater and redirects you to index.html 5 seconds after the timer finishes
@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    if request.method == 'POST':
        # Update score table logic here
        score=request.form.get("score")
        timestamp = datetime.now()
        db.execute("INSERT INTO scores (user_id, score, timestamp) VALUES(?, ?, ?)", session["user_id"], score, timestamp)
        # Redirect to index
        return redirect(url_for('index'))
 
    #call updateTimer function from script.js
    
    return render_template('bowie_game.html')


@socketio.on('timer_finished')
def on_timer_finished(data):
    # This function will be called when the timer finishes
    # You can get the score data from the data dictionary
    score = data['score']
    # Do something with the score data (e.g. save to database)
    emit('redirect', {'url': url_for('game', _external=True)})

#build a route for index.html that gets the higher 10 scores ever with the username, and the score, plus the last score of the user and the higher 10 scores of the user.
@app.route("/", methods=["GET", "POST"])
@login_required
def index():
    if request.method == "GET":
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        lastuserscore = db.execute("SELECT * FROM scores WHERE id = ? ORDER BY timestamp DESC LIMIT 1", session["user_id"])
        higheruserscores = db.execute("SELECT * FROM scores WHERE id = ? ORDER BY score DESC LIMIT 10", session["user_id"])
        return render_template("index.html", username=username, lastuserscore=lastuserscore, higheruserscores=higheruserscores)
    else:
        #button to start the game
        start = request.form.get("start")
        
        return apology("no sé") 

@app.route("/records", methods=["GET"])
@login_required
def records():
    if request.method == "GET":
        higherscores = db.execute("SELECT * FROM scores ORDER BY score DESC LIMIT 10")
        username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        user_records = db.execute("SELECT * FROM scores WHERE id = ? ORDER BY score DESC LIMIT 1", session["user_id"])
        return render_template("records.html", higherscores=higherscores, username=username, user_records=user_records)
    else:
        return apology("no sé") 
    
@app.route("/store", methods=["GET"])
def store():
    if request.method == "GET":
        return apology("Lo siento, no hay nada en la tienda por ahora ")
    else:
        return apology("Lo siento, no hay nada en la tienda por ahora")
    
@app.route("/Bowiecoin", methods=["GET"])
def Bowiecoin():
    if request.method == "GET":
        return apology("EN PROCESO")
    else:
        return apology("EN PROCESO")

# ... other routes ...

#create a route for the game that whill update the database with the score

if __name__ == '__main__':
    app.run(debug=True)

#create a route for the game that whill update the database with the score
