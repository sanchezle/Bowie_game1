from flask import Flask, Response
import requests

import os

from cs50 import SQL
from flask import Flask, flash, redirect, render_template, request, session
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash

from helpers import apology, login_required

import re
app = Flask(__name__)



def fetch_html(url):
    response = requests.get(url)
    return Response(response.text, content_type='text/html; charset=utf-8')

@app.route('/')
def index():
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/templates/index.html"
    return fetch_html(url)

@app.route('/bowiegame')
def bowiegame():
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/templates/bowiegame.html"
    return fetch_html(url)

@app.route('/scores')
def scores():
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/templates/scores.html"
    return fetch_html(url)

@app.route('/instructions')
def instructions():
    url = "https://raw.githubusercontent.com/yourusername/yourrepo/main/templates/instructions.html"
    return fetch_html(url)

if __name__ == '__main__':
    app.run(debug=True)
