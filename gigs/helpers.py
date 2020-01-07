from flask import redirect, render_template, request, session
import requests
from functools import wraps
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

def get_countries():
    with open("gigs/static/countries.json", "r") as read_file:
        countries = json.load(read_file)
        names = []
        for country in countries:
            names.append(country["name"])
        return names

def get_states():
    with open("gigs/static/us_states.json", "r") as read_file:
        states = json.load(read_file)
        names = []
        for state in states:
            names.append(state["name"])
        return names
