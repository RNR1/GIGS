from flask import redirect, render_template, request, session
import requests
from functools import wraps
import sqlite3
from sqlite3 import Error
import json


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

    http://flask.pocoo.org/docs/1.0/patterns/viewdecorators/
    """
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if session.get("user_id") is None:
            return redirect("/login")
        return f(*args, **kwargs)
    return decorated_function


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        if conn:
            conn.close()

def format_datetime(value, format="%d %b %Y"):
    """Format a date time to (Default): d Mon YYYY HH:MM P"""
    if value is None:
        return ""
    return value.strftime(format)


def get_countries():
    # contact API
    try:
        response = requests.get("https://restcountries.eu/rest/v2/all?fields=name")
        response.raise_for_status()
    except requests.RequestException:
        return None

    # Parse response
    try:
        countries = response.json()
        names = []
        for country in countries:
            names.append(country["name"])

        return names
    except (KeyError, TypeError, ValueError):
        return None 

def get_states():
    with open("us_states.json", "r") as read_file:
        states = json.load(read_file)
        names = []
        for state in states:
            names.append(state["name"])
        return names
