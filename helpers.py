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
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_confirmation_email(to_email, subject, html_content):
    gmail_user = os.getenv('GMAIL_USER')  # bowiegame01@gmail.com
    gmail_password = os.getenv('GMAIL_PASSWORD')  # Your Gmail password
    
    if not gmail_user or not gmail_password:
        print("Gmail credentials not configured")
        return False
    
    try:
        # Create message
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = gmail_user
        msg['To'] = to_email
        
        # Add HTML content
        html_part = MIMEText(html_content, 'html')
        msg.attach(html_part)
        
        # Connect to Gmail SMTP server using SSL (port 465)
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(gmail_user, gmail_password)
        
        # Send email
        text = msg.as_string()
        server.sendmail(gmail_user, to_email, text)
        server.quit()
        
        print(f"Email sent successfully to {to_email}")
        return True
        
    except Exception as e:
        print(f"Error sending email: {str(e)}")
        return False


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
