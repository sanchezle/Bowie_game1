import os
import secrets
import uuid
from datetime import datetime, timedelta
import bcrypt
import hashlib

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for, current_app, send_from_directory
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
import jwt


from helpers import apology, login_required, send_confirmation_email,is_valid_password ,save_reset_token, hash_token, verify_token
from flask_socketio import SocketIO, emit
from dotenv import load_dotenv
from email_contents import get_registration_email_content, get_password_reset_email_content, get_user_recovery_email_content


load_dotenv()  # This loads the .env file variables



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
@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return app.send_static_file('sitemap.xml')
@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route("/login", methods=["GET", "POST"])
def login():
    # Forget any user_id
    session.clear()

    if request.method == "POST":
        # Form input validation
        if not request.form.get("identifier"):
            return apology("must provide username", 403)
        elif not request.form.get("password"):
            return apology("must provide password", 403)

        # Query database for username
        identifier = request.form.get("identifier")  # Either username or email
        rows = db.execute("SELECT * FROM users WHERE username = :identifier OR email = :identifier", identifier=identifier)


        # Validate username and password
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], request.form.get("password")):
            return apology("invalid username and/or password", 403)

        # Check if email is confirmed
        if rows[0]["email_confirmed"] == 0:  # In SQLite, False is stored as 0
            return apology("email not confirmed", 403)

        # Set session and redirect user
        session["user_id"] = rows[0]["id"]
        session["instruction_count"] = 3
        return redirect("/")

    else:
        return render_template("login.html")


@app.route("/logout")
def logout():
    """Log user out"""

    # Forget any user_id
    session.clear()

    # Redirect user to login form
    return redirect("/")

 # make sure this is imported from your helpers.py

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")  # Retrieve email from form
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")

        # Validation checks
        if not username:
            return apology("must provide a username", 403)
        if not email:
            return apology("must provide an email", 403)
        if not password:
            return apology("you must provide a password", 403)
        if not confirmation:
            return apology("you must confirm your password", 403)
        if password != confirmation:
            return apology("passwords do not match", 403)
        if not is_valid_password(password):
            return apology('Password must be at least 8 characters long, including at least one letter and one number. Special characters are allowed but not required.', 403)
        # Check if username or email already exists
        count = db.execute("SELECT COUNT(*) as count FROM users WHERE username = ?", username)[0]["count"]
        if count > 0:
            return apology("username already exists", 403)
        email_count = db.execute("SELECT COUNT(*) as count FROM users WHERE email = ?", email)[0]["count"]
        if email_count > 0:
            return apology("email already in use", 403)

        # Hash the password before storing it
        password_hash = generate_password_hash(password)
        verification_token = str(uuid.uuid4())

        # Insert the new user into the database including email and verification token
        db.execute("INSERT INTO users (username, email, hash, verification_token) VALUES(?, ?, ?, ?)",
                   username, email, password_hash, verification_token)
        
        # Generate the verification link
        verification_link = url_for('verify_email', token=verification_token, _external=True)

        # Prepare and send the confirmation email
        subject = "Confirm Your BowieGame Registration"
        html_content = get_registration_email_content(verification_link)
        send_confirmation_email(email, subject, html_content)

        return render_template("success.html")
    
    return render_template("register.html")
    
@app.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
    if request.method == 'POST':
        email = request.form.get('email')

        # Check if user exists in the database
        user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not user:
            flash('No user with the provided email. Please check the email provided.', 'error')
            return render_template('password_reset_request.html')

        # If user exists, proceed with password reset
        secret_key = os.environ.get('SECRET_KEY')
        encoded_jwt = jwt.encode({'email': email, 'exp': datetime.now() + timedelta(minutes=15)}, secret_key, algorithm='HS256')
        reset_link = url_for('reset_password', token=encoded_jwt, _external=True)
        
        # Prepare and send the password reset email
        subject = "Password Reset Request for BowieGame"
        html_content = get_password_reset_email_content(reset_link)
        send_confirmation_email(email, subject, html_content)

        flash('Please check your email to reset your password', 'info')
        
    return render_template('password_reset_request.html')



@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        secret_key = os.environ.get('SECRET_KEY')
        decoded = jwt.decode(token, secret_key, algorithms=['HS256'])
        email = decoded['email']
    except (jwt.ExpiredSignatureError, jwt.InvalidTokenError):
        flash('Invalid or expired token', 'error')
        return redirect(url_for('login'))

    if request.method == 'POST':
        new_password = request.form.get('new_password')
        confirm_password = request.form.get('confirm_password')

        if new_password != confirm_password:
            flash('Passwords do not match', 'error')
            return render_template('reset_password.html', token=token)

        if not is_valid_password(new_password):
            flash('Password does not meet criteria', 'error')
            return render_template('reset_password.html', token=token)

        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ? WHERE email = ?", hashed_password, email)
        flash('Your password has been reset', 'success')
        return redirect(url_for('837834login'))

    return render_template('reset_password.html', token=token)

@app.route('/recover_user', methods=['GET', 'POST'])
def recover_user():
    users_to_recover = db.execute("SELECT username FROM users WHERE email_confirmed = FALSE;")
        
    if request.method == 'POST':
        
        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        token = request.form.get('token')

        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not user:
            return render_template('recover_user.html', message='Non-existing user')

        if new_password != confirmation:
            return render_template('recover_user.html', message='Passwords do not match')

        if not is_valid_password(new_password):
            return render_template('recover_user.html', message='Password must be at least 8 characters long, including at least one letter and one number. Special characters are allowed but not required.')

        hashed_token = user[0]['recover_user_token']
        if not check_password_hash(hashed_token, token):
            return render_template('recover_user.html', message='Wrong recovery user token')

        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ?, recover_user_token = NULL WHERE username = ?", hashed_password, username)

        verification_token = str(uuid.uuid4())
        db.execute("UPDATE users SET verification_token = ? WHERE username = ?", verification_token, username)
        
        # Prepare and send the user recovery email
        recovery_link = url_for('verify_email', token=verification_token, _external=True)
        subject = "User Recovery Confirmation"
        html_content = get_user_recovery_email_content(recovery_link)
        send_confirmation_email(email, subject, html_content)

        return render_template( 'recover_user.html', users_to_recover=users_to_recover, message='Please check your email to confirm your email, otherwise you will not be able to login')

    return render_template('recover_user.html',  users_to_recover=users_to_recover)


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
        higherscores = db.execute("SELECT username, score, timestamp, RANK() OVER (ORDER BY max_scores.max_score DESC) AS rank FROM (SELECT user_id, MAX(score) AS max_score FROM scores GROUP BY user_id) AS max_scores JOIN scores ON max_scores.user_id = scores.user_id AND max_scores.max_score = scores.score JOIN users ON scores.user_id = users.id ORDER BY max_scores.max_score DESC LIMIT 20")
            #""""
        user_records = db.execute("SELECT username, score, timestamp, RANK() OVER (ORDER BY score DESC) AS rank FROM scores JOIN users ON scores.user_id = users.id  WHERE scores.user_id = ? ORDER BY score DESC LIMIT 5", session["user_id"])
        username_dic = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])
        username = username_dic[0]["username"]
       
        return render_template("records.html", higherscores=higherscores, username=username, user_records=user_records)
    else:
        return apology("no sé") 


@app.route('/verify_email/<token>')
def verify_email(token):
    # Query the database to find the user with this token
    user = db.execute("SELECT * FROM users WHERE verification_token = ?", token)
    if user:
        # Update the isVerified column for this user
        db.execute("UPDATE users SET email_confirmed = TRUE, verification_token = NULL WHERE verification_token = ?", token)
        
        # Render a template on successful verification
        return render_template('email_verified.html')
    else:
        # Handle invalid or expired token
        return "Invalid or expired verification link."



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



if __name__ == '__main__':
    app.run(debug=True)


