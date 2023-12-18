import os


from flask import redirect, render_template, request, session
from functools import wraps
from dotenv import load_dotenv

import re
load_dotenv()

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


# helpers.py

# helpers.py
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail

import os
import requests
def send_confirmation_email(to_email, subject, verification_link):
    api_key = os.getenv('MAILERSEND_API_KEY')
    from_email = os.getenv('FROM_EMAIL')  # Retrieve the sender's email from environment variable
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    data = {
        "from": {
            "email": from_email,
            "name": "Bowiegame"  # Optionally, update this as well
        },
        "to": [
            {
                "email": to_email
            }
        ],
        "subject": subject,
        "html": f"<p>Please confirm your email by clicking on this <a href='{verification_link}'>link</a>.</p>"
    }

    response = requests.post("https://api.mailersend.com/v1/email", json=data, headers=headers)
    return response
