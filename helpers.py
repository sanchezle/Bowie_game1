import os
import requests
import urllib.parse

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

def send_confirmation_email(to_email, subject, verification_link):
    api_key = os.getenv('SENDGRID_API_KEY')
    from_email = os.getenv('SENDGRID_FROM_EMAIL')  # Retrieve the sender's email from environment variable

    sendgrid_client = SendGridAPIClient(api_key)
    content = f"<p>Please confirm your email by clicking on this <a href='{verification_link}'>link</a>.</p>"

    message = Mail(
        from_email=from_email,
        to_emails=to_email,
        subject=subject,
        html_content=content
    )

    # In your send_confirmation_email function
    try:
        response = sendgrid_client.send(message)
        print(response.status_code)
        print(response.body)
        print(response.headers)
    except Exception as e:
        print(str(e))  # Corrected exception handling