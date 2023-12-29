import os


from flask import redirect, render_template, request, session
from functools import wraps
from dotenv import load_dotenv

import re
load_dotenv()
import re
def apology(message, code=400):
    """Render message as an apology to user."""
    def escape(s):
        """
        Escape special characters.

        https://github.com/jacebrowning/memegen#special-characters
        """
        for old, new in [("-", "--"), (" ", "-"), ("_", "__"), ("?", "~q"),
                         ("%", "~p"), ("#", "~h"), ("/", "~s"), ("\"", "''")]:
            s = s.replace(old, new)
        return s
    return render_template("apology.html", top=code, bottom=escape(message)), code


def login_required(f):
    """
    Decorate routes to require login.

    https://flask.palletsprojects.com/en/1.1.x/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def is_valid_password(password):
    # Define the regex pattern for the password
    pattern = r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d!@#$%^&*()_+-=]{8,}$'  # Updated pattern
    return re.match(pattern, password) is not None


# helpers.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

def send_confirmation_email(to_email, subject, html_content):
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = os.getenv('SENDGRID_FROM_EMAIL')  # Retrieve the sender's email from environment variable

    sendgrid_client = SendGridAPIClient(api_key)

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=html_content
    )

    # Sending the email
    try:
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))  # Improved exception handling


import bcrypt

def hash_token(token):
    return bcrypt.hashpw(token.encode(), bcrypt.gensalt())

def verify_token(provided_token, stored_hash):
    return bcrypt.checkpw(provided_token.encode(), stored_hash)

def save_reset_token(email, hashed_token, expiry):
    # Logic to update the user's record in the database
    user = User.query.filter_by(email=email).first()
    if user:
        user.reset_token = hashed_token
        user.reset_token_expiry = expiry
        db.session.commit()
