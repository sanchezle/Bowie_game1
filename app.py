import os
from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, Response, jsonify, url_for
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
        
              # Initialize the instruction counter
        session["instruction_count"] = 3
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





# q: when the '/updatescore' route is going to be calle?
# a
# just renders the templater and redirects you to index.html 5 seconds after the timer finishes
@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    if request.method == 'GET':
        # Show instructions if the counter is greater than 0
        show_instructions = session.get('instruction_count', 0) > 0
        if show_instructions:
            # Decrement the counter
            session['instruction_count'] -= 1
        return render_template('bowie_game.html', show_instructions=show_instructions)
    if request.method == 'POST':
        # Update score table logic here
        score = request.json.get('score')
        timestamp = datetime.now()
        db.execute("INSERT INTO scores (user_id, score, timestamp) VALUES(?, ?, ?)", session["user_id"], score, timestamp)
        # Redirect to index
         # Create the response dictionary
        response = {
                    'message': 'Score updated successfully',
            'redirect': url_for('index')
        }
        
        # Redirect the user to the index page
        return jsonify(response)

    #call updateTimer function from script.js

    return render_template('bowie_game.html')

@app.route('/game2', methods=['GET', 'POST'])
@login_required
def game2():
    if request.method == 'POST':
        # Update score table logic here
        score = request.json.get('score')
        timestamp = datetime.now()
        db.execute("INSERT INTO scores (user_id, score, timestamp) VALUES(?, ?, ?)", session["user_id"], score, timestamp)
        # Redirect to index
         # Create the response dictionary
        response = {
                    'message': 'Score updated successfully',
            'redirect': url_for('index')
        }
        
        # Redirect the user to the index page
        return jsonify(response)

    #call updateTimer function from script.js

    return render_template('test.html')


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
        #get the user id from the session
        user_id = session["user_id"]
        #get the username from the user id
        username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
        #join the scores table with the users table to get the username and the score and timestamp of the last score of the user
        lastuserscore_dic= db.execute("SELECT score, timestamp, username FROM scores JOIN users ON scores.user_id = users.id WHERE scores.user_id = ? ORDER BY timestamp DESC LIMIT 1", user_id)

        if lastuserscore_dic:
            lastuserscore = lastuserscore_dic[0]["score"]
        else:
            lastuserscore = 0
       
        #join the scores table with the users table to get the username and the score and timestamp of the 5 higher scores of the user
        higheruserscores = db.execute("SELECT username, score, timestamp, RANK() OVER (ORDER BY score DESC) AS rank FROM scores JOIN users ON scores.user_id = users.id  WHERE scores.user_id = ? ORDER BY score DESC LIMIT 5", user_id)
        return render_template("index.html", username=username, lastuserscore=lastuserscore, higheruserscores=higheruserscores)
    else:
        #button to start the game
        start = request.form.get("start")
        
        return apology("no sé") 

@app.route("/records", methods=["GET"])
@login_required
def records():
    if request.method == "GET":
        #join the scores table with the users table to get the a rank, username, score and timestamp of the 10 higher scores ever
        higherscores = db.execute("SELECT username, score, timestamp, RANK() OVER (ORDER BY score DESC) AS rank FROM scores JOIN users ON scores.user_id = users.id ORDER BY score DESC LIMIT 10")
        #long comment notation with cuotes and line breaks """higherscores = db.execute("SELECT users.username, max_scores.max_score, scores.timestamp, 
            #RANK() OVER (ORDER BY max_scores.max_score DESC) AS rank
            #FROM (
                #SELECT user_id, MAX(score) AS max_score
                #FROM scores
                #GROUP BY user_id
            #) AS max_scores
            #JOIN scores ON max_scores.user_id = scores.user_id AND max_scores.max_score = scores.score
            #JOIN users ON scores.user_id = users.id
            #ORDER BY max_scores.max_score DESC
            #LIMIT 10
            #")
            #""""
        user_records = db.execute("SELECT username, score, timestamp, RANK() OVER (ORDER BY score DESC) AS rank FROM scores JOIN users ON scores.user_id = users.id  WHERE scores.user_id = ? ORDER BY score DESC LIMIT 5", session["user_id"])
        username_dic = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username_dic[0]["username"]
       
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

@app.route('/instructions', methods=['GET'])
@login_required
def instructions():
    return render_template('instructions.html')

@app.route('/update_instructions', methods=['POST'])
@login_required
def update_instructions():
    if request.form.get('no_instructions') == 'on':
        session['instruction_count'] = 0
    return redirect(url_for('game'))


#create a route for the game that whill update the database with the score

if __name__ == '__main__':
    app.run(debug=True)

#create a route for the game that whill update the database with the score
