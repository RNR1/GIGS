from flask import Flask, request, render_template, redirect, session, g
from .helpers import apology, login_required, create_connection, format_datetime, get_countries, get_states
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.exceptions import default_exceptions, HTTPException, InternalServerError
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3
import os
import psycopg2
from .user import User
from .gig import Gig

def create_app(config_file='settings.py'):
    app = Flask(__name__)

    app.config.from_pyfile(config_file)

    DATABASE_URL = os.environ.get('DATABASE_URL')
    conn = psycopg2.connect(DATABASE_URL, sslmode='require')
    db = conn.cursor()


    # Ensure responses aren't cached
    # @app.after_request
    # def after_request(response):
    #     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    #     response.headers["Expires"] = 0
    #     response.headers["Pragma"] = "no-cache"
    #     return response

    # # Register the template filter with the Jinja Environment
    # app.jinja_env.filters['formatdatetime'] = format_datetime


    # # Configure session to use filesystem (instead of signed cookies)
    # app.config["SESSION_FILE_DIR"] = mkdtemp()
    # app.config["SESSION_PERMANENT"] = False
    # app.config["SESSION_TYPE"] = "filesystem"
    # Session(app)

    # TEMPLATES
    ## index
    @app.route('/')
    def index():
        """Landing page"""
        return render_template('index.html')

    ## account
    @app.route('/account', methods=["GET", "POST"])
    @login_required
    def account():
        """acount settings"""
        db.execute("SELECT * FROM users WHERE id = :id", {'id': session["user_id"]})
        row = db.fetchone()

        return render_template('account.html', message=False, display=row[3])

    ## add Gig
    @app.route('/add', methods=["GET", "POST"])
    @login_required
    def add():
        """add GIG"""
        if request.method == "POST":
            form = request.form.get

            # VALIDATIONS:
            if not form('date'):
                return apology("must specify date")
            elif not form('venue'):
                return apology("must specify venue name")
            elif not form('city'):
                return apology("must specify city")
            elif not form('country'):
                return apology("must specify country")
        
            gig = Gig(session["user_id"], form('date'), form('time'), form('venue'), form('event'), form('city'), form('state'), form('country'))
        
        # add to db
            try:
                db.execute("INSERT INTO gigs(user, date, venue, event, city, state, country, time) VALUES (:user, :date, :venue, :event, :city, :state, :country, :time)", 
                {'user': gig.user, 'date': gig.date, 'venue': gig.venue, 'event': gig.event, 'city': gig.location['city'], 'state': gig.location['state'], 'country': gig.location['country'], 'time': gig.time})
            except: 
                return apology("Invalid request")
            finally:
                conn.commit()
                return redirect('/profile')
        
        else:        
            return render_template('add.html', countries=get_countries(), states=get_states())

    ## Login
    @app.route('/login', methods=["GET", "POST"])
    def login():
        """login form"""
        # Forget any user_id
        session.clear()

        # POST
        if request.method == "POST":

            # Ensure username was submitted
            if not request.form.get("email"):
                return apology("must provide username", 403)

            # Ensure password was submitted
            elif not request.form.get("password"):
                return apology("must provide password", 403)

            # Query database for username
            db.execute("SELECT * FROM users WHERE email = :email",
                              {'email': request.form.get("email")})
            rows = db.fetchall()
        
            if len(rows) != 1 or not check_password_hash(rows[0][2], request.form.get("password")):
                return apology("invalid username and/or password", 403)           

            # Remember which user has logged in
            session["user_id"] = rows[0][0]
            # Redirect user to home page
            return redirect("/profile")

        # GET
        else: 
            return render_template('login.html')    

    @app.route('/register', methods=["GET", "POST"])
    def register():
        """register form""" 
        # method="POST"
        if request.method == "POST":
        
            # Store user input data
            form = request.form.get
            email = form("email")
            password = form("password")
            confirmation = form("password-confirmation")
   
            # VALIDATIONS:
            if not email:
                return apology("must provide email")
            elif not password:
                return apology("must provide password")
            elif not confirmation or confirmation != password:
                return apology("Password's confirmation does not match")

            # Hash the user’s password with generate_password_hash
            hash = password
            user = User(form("email"), form('display-name'), form('first-name'), form('last-name'), form('city'), form('state'), form('country'), form('bio'))

            # add to db
            try:
                db.execute("INSERT INTO users(email, hash, display, first, last, city, state, country, bio) VALUES (:email, :hash, :display, :first, :last, :city, :state, :country, :bio)", 
                {'email': user.email, 'hash': hash, 'display': user.display, 'first': user.first, 'last': user.last, 'city': user.location['city'], 'state': user.location['state'], 'country': user.location['country'], 'bio': user.bio})
            except: 
                return apology("user already exists")
            finally:
                conn.commit()

            # Query database for username
            db.execute("SELECT * FROM users WHERE email = :email", {'email': user.email})        

            row = db.fetchone() 

            # Remember which user has logged in
            session["user_id"] = row[0]
            return redirect('/')    

        else:
            # method="GET"
            return render_template('register.html')

    @app.route("/logout")
    def logout():
        """Log user out"""

        # Forget any user_id
        session.clear()

        # Redirect user to login form
        return redirect("/")

    @app.route('/profile', methods=["GET", "DELETE"])
    @login_required
    def profile():
        """personal profile""" 

        # Get user profile info
        db.execute("SELECT * FROM users WHERE id = :id", {'id': session["user_id"]})
        row = db.fetchone()
    
        #Get user gigs
        db.execute("SELECT * FROM gigs WHERE user = :user ORDER BY date ASC", {'user': session["user_id"]})
        gigs = db.fetchall()


        # arrange user profile info
        display = row[3]
        name = '{} {}'.format(row[4], row[5])
        state = row[7]
        bio = row[10]
        if len(state) is 0:
            location = '{}, {}'.format(row[6], row[8])
        else:
            location = '{}, {}, {}'.format(row[6], row[7], row[8])
    
        return render_template('profile.html', display=display, name=name, location=location, gigs=gigs, bio=bio)
 
    @app.route('/remove/<id>', methods=["POST"])
    def remove(id):
        """remove gig from profile"""
        try:
            db.execute("DELETE FROM gigs WHERE id = :id", {'id': id})
        except: 
            return apology("can't delete")
        finally:
            conn.commit()
    
        return redirect('/profile')

    @app.route('/delete_account', methods=["POST"])
    def delete_account():
        print('remove')
        try:
            db.execute("DELETE FROM users WHERE id = :id", {'id': session["user_id"]})
        except: 
            return apology("can't delete")
        finally:
            conn.commit()
    
        return redirect("/logout")

    @app.route('/change_login', methods=["POST"])
    def change_login():
        email = request.form.get('email')
        password = request.form.get('password')
    
        if password:
            hash = generate_password_hash(password)
            try:
                db.execute("UPDATE users SET hash = :hash WHERE id = :id", {'hash': hash, 'id': session["user_id"]})
            except: 
                return apology("problem updating password")
        if email:
            try:
                db.execute("UPDATE users SET email = :email WHERE id = :id", {'email': email, 'id': session["user_id"]})
            except: 
                return apology("problem updating email")

        conn.commit()    
        return render_template('account.html', message="Login information updated successfully!")

    @app.route('/change_bio', methods=["POST"])
    def bio():
        bio = request.form.get('bio')

        if bio:
            try:
                db.execute("UPDATE users SET bio = :bio WHERE id = :id", {'bio': bio, 'id': session["user_id"]})
            except:
                return apology("problem updating bio")

        return redirect('/profile')

    return app