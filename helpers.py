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

import requests

def send_confirmation_email(to_email, subject, verification_link):
    api_key = os.getenv('MAILJET_API_KEY')
    api_secret = os.getenv('MAILJET_API_SECRET')
    headers = {
        "Content-Type": "application/json"
    }
    data = {
        "Messages": [
            {
                "From": {
                    "Email": os.getenv('FROM_EMAIL'),
                    "Name": "bowiegame"
                },
                "To": [
                    {
                        "Email": to_email
                    }
                ],
                "Subject": subject,
                "HTMLPart": f"<p>Please confirm your email by clicking on this <a href='{verification_link}'>link</a>.</p>"
            }
        ]
    }

    response = requests.post("https://api.mailjet.com/v3.1/send", auth=(api_key, api_secret), json=data, headers=headers)
    return response
