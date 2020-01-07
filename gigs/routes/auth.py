from flask import Blueprint, render_template, request, redirect, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
from gigs.helpers import apology, get_countries, get_states
from gigs.extensions import conn, db
from gigs.models import Gig, User

auth = Blueprint('auth', __name__)

@auth.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        
        form = request.form.get
        email = form("email")
        password = form("password")
        confirmation = form("password-confirmation")
   
        if not email:
            return apology("must provide email")
        elif not password:
            return apology("must provide password")
        elif not confirmation or confirmation != password:
            return apology("Password's confirmation does not match")

        hash = generate_password_hash(password)
        user = User(form("email"), form('display-name'), form('first-name'), form('last-name'), form('city'), form('state'), form('country'), form('bio'))

        try:
            db.execute("""INSERT INTO users(email, hash, display, first, last, city, state, country, bio) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')"""
            .format(user.email, hash, user.display, user.first, user.last, user.location['city'], user.location['state'], user.location['country'], user.bio))
        except Exception as e:
            print(e) 
            return apology("user already exists")
        finally:
            conn.commit()

        db.execute("SELECT * FROM users WHERE email = '{}'".format(user.email))        
        row = db.fetchone() 

        session["user_id"] = row[0]
        return redirect('/')    

    return render_template('register.html')

@auth.route('/login', methods=["GET", "POST"])
def login():
    session.clear()

    if request.method == "POST":

        if not request.form.get("email"):
            return apology("must provide username", 403)

        elif not request.form.get("password"):
            return apology("must provide password", 403)

        db.execute("SELECT * FROM users WHERE email = '{}'".format(request.form.get("email")))
        rows = db.fetchall()
        if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
            return apology("invalid username and/or password", 403)           

        session["user_id"] = rows[0][0]
        return redirect("/profile")

    return render_template('login.html')    

@auth.route('/change_login', methods=["POST"])
def change_login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    if not password and not email:
        return apology("all fields are required", 400)

    if password:
        hash = generate_password_hash(password)
        try:
            db.execute("UPDATE users SET hash = '{}' WHERE id = '{}'".format(hash, session["user_id"]))
        except: 
            return apology("problem updating password")
    if email:
        try:
            db.execute("UPDATE users SET email = '{}' WHERE id = '{}'".format(email, session["user_id"]))
        except: 
            return apology("problem updating email")

    conn.commit()    
    return render_template('account.html', message="Login information updated successfully!")

@auth.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('auth.login'))