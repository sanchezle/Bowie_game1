import os
import secrets
import uuid
from datetime import datetime, timedelta

import bcrypt
import hashlib
import jwt
from flask import Flask, flash, redirect, render_template, request, session, jsonify, url_for, send_from_directory, g
from flask_session import Session
from werkzeug.security import check_password_hash, generate_password_hash
from flask_socketio import SocketIO, emit
from cs50 import SQL
from dotenv import load_dotenv
from authlib.integrations.flask_client import OAuth
from helpers import apology, login_required, send_confirmation_email, is_valid_password
from email_contents import get_registration_email_content, get_password_reset_email_content, get_user_recovery_email_content

load_dotenv()

# Flask app configuration

app = Flask(__name__)
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
socketio = SocketIO(app)

# OAuth configuration
oauth = OAuth(app)

google = oauth.register(
    name='google',
    client_id=os.getenv('GOOGLE_CLIENT_ID'),
    client_secret=os.getenv('GOOGLE_CLIENT_SECRET'),
    access_token_url='https://oauth2.googleapis.com/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    client_kwargs={
        'scope': 'openid email profile',
        'claims_options': {
            'iss': {'values': ['https://accounts.google.com', 'accounts.google.com']}
        }
    },
    server_metadata_url='https://accounts.google.com/.well-known/openid-configuration'
)

facebook = oauth.register(
    name='facebook',
    client_id=os.getenv('FACEBOOK_CLIENT_ID'),
    client_secret=os.getenv('FACEBOOK_CLIENT_SECRET'),
    access_token_url='https://graph.facebook.com/v9.0/oauth/access_token',
    authorize_url='https://www.facebook.com/v9.0/dialog/oauth',
    client_kwargs={'scope': 'email'}
)




# Database configuration
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE = os.path.join(BASE_DIR, "bowiegame.db")
db = SQL(f"sqlite:///{DATABASE}")

# Utility functions for database connection
def get_db():
    if not hasattr(g, '_database'):
        g._database = sqlite3.connect(DATABASE)
    return g._database

def generate_provisional_username(base):
    attempt = 1
    while True:
        provisional_username = f"{base}{attempt}"
        result = db.execute("SELECT COUNT(*) as count FROM users WHERE username = ?", [provisional_username])
        if result and result[0].get('count') == 0:
            break
        attempt += 1
    return provisional_username

@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

# OAuth Routes
@app.route('/login/google')
def login_google():
    nonce = secrets.token_urlsafe()
    session['nonce'] = nonce
    redirect_uri = url_for('authorize_google', _external=True)
    return google.authorize_redirect(redirect_uri, nonce=nonce)

@app.route('/authorize/google')
def authorize_google():
    token = google.authorize_access_token()
    nonce = session.pop('nonce', None)
    user_info = google.parse_id_token(token, nonce)
    email = user_info['email']
    oauth_id = user_info['sub']
    user = db.execute("SELECT * FROM users WHERE email = ? AND oauth_provider = 'google'", email)

    if not user:
        base_username = user_info['name'].split()[0].lower()  # Using first name as base for username
        username = generate_provisional_username(base_username)
        db.execute("INSERT INTO users (username, email, oauth_provider, oauth_id, email_confirmed) VALUES (?, ?, 'google', ?, TRUE)", username, email, oauth_id)
        user = db.execute("SELECT * FROM users WHERE email = ? AND oauth_provider = 'google'", email)

    session["user_id"] = user[0]["id"]
    return redirect(url_for('index'))

@app.route('/authorize/facebook')
def authorize_facebook():
    token = facebook.authorize_access_token()
    user_info = facebook.get('https://graph.facebook.com/me?fields=id,name,email', token=token).json()
    email = user_info['email']
    oauth_id = user_info['id']
    user = db.execute("SELECT * FROM users WHERE email = ? AND oauth_provider = 'facebook'", email)

    if not user:
        base_username = user_info['name'].split()[0].lower()  # Using first name as base for username
        username = generate_provisional_username(base_username)
        db.execute("INSERT INTO users (username, email, oauth_provider, oauth_id, email_confirmed) VALUES (?, ?, 'facebook', ?, TRUE)", username, email, oauth_id)
        user = db.execute("SELECT * FROM users WHERE email = ? AND oauth_provider = 'facebook'", email)

    session["user_id"] = user[0]["id"]
    return redirect(url_for('index'))


@app.route('/login/facebook')
def login_facebook():
    redirect_uri = url_for('authorize_facebook', _external=True)
    return facebook.authorize_redirect(redirect_uri)


# Routes
@app.route('/')
@login_required
def index():
    user_id = session["user_id"]
    username = db.execute("SELECT username FROM users WHERE id = ?", user_id)[0]["username"]
    last_score_data = db.execute("SELECT score, timestamp FROM scores WHERE user_id = ? ORDER BY timestamp DESC LIMIT 1", user_id)
    last_score = last_score_data[0]["score"] if last_score_data else 0
    user_scores = db.execute("SELECT score, timestamp FROM scores WHERE user_id = ? ORDER BY score DESC LIMIT 5", user_id)
    return render_template("index.html", username=username, last_score=last_score, user_scores=user_scores)

@app.route('/users')
def get_users():
    cur = get_db().cursor()
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return jsonify(users)

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.clear()
    if request.method == 'POST':
        identifier = request.form.get("identifier")
        password = request.form.get("password")
        if not identifier or not password:
            return apology("must provide username and password", 403)
        rows = db.execute("SELECT * FROM users WHERE username = :identifier OR email = :identifier", identifier=identifier)
        if len(rows) != 1 or not check_password_hash(rows[0]["hash"], password):
            return apology("invalid username and/or password", 403)
        if not rows[0]["email_confirmed"]:
            return apology("email not confirmed", 403)
        session["user_id"] = rows[0]["id"]
        session["instruction_count"] = 3
        return redirect("/")
    return render_template("login.html")

@app.route('/logout')
def logout():
    session.clear()
    return redirect("/")

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        confirmation = request.form.get("confirmation")
        if not all([username, email, password, confirmation]):
            return apology("all fields are required", 403)
        if password != confirmation:
            return apology("passwords do not match", 403)
        if not is_valid_password(password):
            return apology('Password must be at least 8 characters long, including at least one letter and one number.', 403)
        if db.execute("SELECT COUNT(*) FROM users WHERE username = ?", username)[0]["count"] > 0:
            return apology("username already exists", 403)
        if db.execute("SELECT COUNT(*) FROM users WHERE email = ?", email)[0]["count"] > 0:
            return apology("email already in use", 403)
        password_hash = generate_password_hash(password)
        verification_token = str(uuid.uuid4())
        db.execute("INSERT INTO users (username, email, hash, verification_token) VALUES(?, ?, ?, ?)", username, email, password_hash, verification_token)
        verification_link = url_for('verify_email', token=verification_token, _external=True)
        send_confirmation_email(email, "Confirm Your BowieGame Registration", get_registration_email_content(verification_link))
        return render_template("success.html")
    return render_template("register.html")

@app.route('/password_reset_request', methods=['GET', 'POST'])
def password_reset_request():
    if request.method == 'POST':
        email = request.form.get('email')
        user = db.execute("SELECT * FROM users WHERE email = ?", email)
        if not user:
            flash('No user with the provided email.', 'error')
            return render_template('password_reset_request.html')
        secret_key = os.getenv('SECRET_KEY')
        token = jwt.encode({'email': email, 'exp': datetime.utcnow() + timedelta(minutes=15)}, secret_key, algorithm='HS256')
        reset_link = url_for('reset_password', token=token, _external=True)
        send_confirmation_email(email, "Password Reset Request for BowieGame", get_password_reset_email_content(reset_link))
        flash('Please check your email to reset your password', 'info')
    return render_template('password_reset_request.html')

@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    try:
        secret_key = os.getenv('SECRET_KEY')
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
        return redirect(url_for('login'))
    return render_template('reset_password.html', token=token)

@app.route('/recover_user', methods=['GET', 'POST'])
def recover_user():
    users_to_recover = db.execute("SELECT username FROM users WHERE email_confirmed = 0")
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        new_password = request.form.get('password')
        confirmation = request.form.get('confirmation')
        token = request.form.get('token')
        user = db.execute("SELECT * FROM users WHERE username = ?", username)
        if not user:
            return render_template('recover_user.html', message='Non-existing user', users_to_recover=users_to_recover)
        if new_password != confirmation:
            return render_template('recover_user.html', message='Passwords do not match', users_to_recover=users_to_recover)
        if not is_valid_password(new_password):
            return render_template('recover_user.html', message='Invalid password', users_to_recover=users_to_recover)
        if not check_password_hash(user[0]['recover_user_token'], token):
            return render_template('recover_user.html', message='Invalid token', users_to_recover=users_to_recover)
        hashed_password = generate_password_hash(new_password)
        db.execute("UPDATE users SET hash = ?, recover_user_token = NULL WHERE username = ?", hashed_password, username)
        verification_token = str.uuid.uuid4()
        db.execute("UPDATE users SET verification_token = ? WHERE username = ?", verification_token, username)
        recovery_link = url_for('verify_email', token=verification_token, _external=True)
        send_confirmation_email(email, "User Recovery Confirmation", get_user_recovery_email_content(recovery_link))
        return render_template('recover_user.html', users_to_recover=users_to_recover, message='Please check your email to confirm your email')
    return render_template('recover_user.html', users_to_recover=users_to_recover)

@app.route('/game', methods=['GET', 'POST'])
@login_required
def game():
    if request.method == 'GET':
        show_instructions = session.get('instruction_count', 0) > 0
        if show_instructions:
            session['instruction_count'] -= 1
        return render_template('bowie_game.html', show_instructions=show_instructions)
    if request.method == 'POST':
        score = request.json.get('score')
        timestamp = datetime.now()
        db.execute("INSERT INTO scores (user_id, score, timestamp) VALUES (?, ?, ?)", session["user_id"], score, timestamp)
        response = {'message': 'Score updated successfully', 'redirect': url_for('index')}
        return jsonify(response)

@socketio.on('timer_finished')
def on_timer_finished(data):
    score = data['score']
    emit('redirect', {'url': url_for('game', _external=True)})

@app.route('/records', methods=['GET'])
@login_required
def records():
    higherscores = db.execute("SELECT username, score, timestamp FROM (SELECT user_id, MAX(score) AS max_score FROM scores GROUP BY user_id) max_scores JOIN scores ON max_scores.user_id = scores.user_id AND max_scores.max_score = scores.score JOIN users ON scores.user_id = users.id ORDER BY max_scores.max_score DESC LIMIT 20")
    user_records = db.execute("SELECT score, timestamp FROM scores WHERE user_id = ? ORDER BY score DESC LIMIT 5", session["user_id"])
    username = db.execute("SELECT username FROM users WHERE id = ?", session["user_id"])[0]["username"]
    return render_template("records.html", higherscores=higherscores, username=username, user_records=user_records)

@app.route('/verify_email/<token>')
def verify_email(token):
    user = db.execute("SELECT * FROM users WHERE verification_token = ?", token)
    if user:
        db.execute("UPDATE users SET email_confirmed = 1, verification_token = NULL WHERE verification_token = ?", token)
        return render_template('email_verified.html')
    return "Invalid or expired verification link."

@app.route('/sitemap.xml', methods=['GET'])
def sitemap():
    return app.send_static_file('sitemap.xml')

@app.route('/robots.txt')
def robots_txt():
    return send_from_directory(app.static_folder, request.path[1:])

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/store', methods=['GET'])
def store():
    return apology("Lo siento, no hay nada en la tienda por ahora ")

@app.route('/Bowiecoin', methods=['GET'])
def Bowiecoin():
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

