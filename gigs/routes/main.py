from flask import Blueprint, render_template, request, redirect, session, url_for
from gigs.helpers import login_required, apology, get_countries, get_states
from gigs.extensions import conn, db
from gigs.models import Gig, User

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/account', methods=["GET", "POST"])
@login_required
def account():
    db.execute("SELECT * FROM users WHERE id = '{}'".format(session["user_id"]))
    row = db.fetchone()

    return render_template('account.html', message=False, display=row[3])

@main.route('/add', methods=["GET", "POST"])
@login_required
def add():
    if request.method == "POST":
        form = request.form.get

        if not form('date'):
            return apology("must specify date")
        elif not form('venue'):
            return apology("must specify venue name")
        elif not form('city'):
            return apology("must specify city")
        elif not form('country'):
            return apology("must specify country")
        
        gig = Gig(session["user_id"], form('date'), form('time'), form('venue'), form('event'), form('city'), form('state'), form('country'))
        
        try:
            db.execute("""INSERT INTO gigs(user_id, date, venue, event, city, state, country, time) VALUES ('{}', '{}', '{}', '{}', '{}', '{}', '{}', '{}')""".format(gig.user_id, gig.date, gig.venue, gig.event, gig.location['city'], gig.location['state'], gig.location['country'], gig.time))
        except Exception as error:
            print(error) 
            return apology("Invalid request")
        finally:
            conn.commit()
                
        return redirect(url_for('main.profile'))
        
      
    return render_template('add.html', countries=get_countries(), states=get_states())

    
@main.route('/profile', methods=["GET", "DELETE"])
@login_required
def profile():
    db.execute("SELECT * FROM users WHERE id = '{}'".format(session["user_id"]))
    row = db.fetchone()
    
    db.execute("SELECT * FROM gigs WHERE user_id = '{}' ORDER BY date ASC".format(session["user_id"]))
    gigs = db.fetchall()

    display = row[3]
    name = '{} {}'.format(row[4], row[5])
    state = row[7]
    bio = row[10]
    if len(state) is 0:
        location = '{}, {}'.format(row[6], row[8])
    else:
        location = '{}, {}, {}'.format(row[6], row[7], row[8])
    
    return render_template('profile.html', display=display, name=name, location=location, gigs=gigs, bio=bio)
 
@main.route('/remove/<id>', methods=["POST"])
def remove(id):
    try:
        db.execute("DELETE FROM gigs WHERE id = '{}'".format(id))
    except: 
        return apology("can't delete")
    finally:
        conn.commit()
    
    return redirect(url_for('main.profile'))

@main.route('/delete_account', methods=["POST"])
def delete_account():
    try:
        db.execute("DELETE FROM users WHERE id = '{}'".format(session["user_id"]))
    except: 
        return apology("can't delete")
    finally:
        conn.commit()
    
    return redirect(url_for('auth.logout'))


@main.route('/change_bio', methods=["POST"])
def bio():
    bio = request.form.get('bio')

    if bio:
        try:
            db.execute("UPDATE users SET bio = '{}' WHERE id = '{}'".format(bio, session["user_id"]))
        except:
            return apology("problem updating bio")

    return redirect(url_for('main.profile'))