from flask import Flask, render_template, request, redirect, session, send_file
import sqlite3
import os
import time
from waitress import serve
from dotenv import load_dotenv
import bcrypt



app = Flask(__name__)


load_dotenv() #this gives access .env file

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')






# ---------------------------------------------------------
# SESSION MANAGEMENT VULNERABILITY
# ---------------------------------------------------------
# Hardcoded secret key.
# If an attacker obtains this key, they can forge session cookies.
# Proper systems store this securely in environment variables.
# ---------------------------------------------------------
#completed
print("go to the link shown below to reach your stupid website")
print("http://localhost:8000/")



@app.route('/')
def login():
    return render_template('login.html')


@app.route('/login_validation', methods=['POST'])
def login_validation():

    email = request.form.get('email')
    password = request.form.get('password')

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()

    # ---------------------------------------------------------
    # SQL INJECTION VULNERABILITY
    # ---------------------------------------------------------
    # This query directly inserts user input into SQL.
    # An attacker could enter:
    # email: ' OR '1'='1
    # password: anything
    # This would log them in without knowing credentials.
    # ---------------------------------------------------------
    #completed

    query = "SELECT * FROM USERS WHERE email = ?"
    user = cursor.execute(query, (email,)).fetchone()
    connection.close()

    time.sleep(1)

    # ---------------------------------------------------------
    # SIDE CHANNEL ATTACK (Timing Attack)
    # ---------------------------------------------------------
    # This artificial delay creates measurable timing differences.
    # Attackers could measure response times to guess valid emails.
    # ---------------------------------------------------------
    #completed
    if user and bcrypt.checkpw(password.encode('utf-8'), user[3]):
        
        session.clear() 
        session['user'] = email
        return redirect(f'/home?fname={user[0]}&lname={user[1]}&email={user[2]}')

    
    return redirect('/')


        # ---------------------------------------------------------
        # BROKEN AUTHENTICATION
        # ---------------------------------------------------------
        # Passwords are stored in plain text.
        # No hashing, no salting.
        # If DB is leaked, all passwords are exposed.
        # ---------------------------------------------------------
        #completed

        # ---------------------------------------------------------
        # SESSION MANAGEMENT VULNERABILITY
        # ---------------------------------------------------------
        # Storing email directly in session without regeneration.
        # Session fixation possible.
        # ---------------------------------------------------------
        


@app.route('/signUp')
def signUp():
    return render_template('signUp.html')


@app.route('/home')
def home():

    if 'user' not in session:
        return redirect('/')


    email = session.get('user')
    fname = request.args.get('fname')
    lname = request.args.get('lname')
    
    return render_template('home.html', fname=fname, lname=lname, email=email)


    # ---------------------------------------------------------
    # BROKEN AUTHENTICATION
    # ---------------------------------------------------------
    # No check that a valid session exists.
    # Anyone can manually visit:
    # http://site/home?fname=Admin&lname=User&email=admin@email.com
    # and appear logged in.
    # ---------------------------------------------------------
    #completed


    # ---------------------------------------------------------
    # CROSS-SITE SCRIPTING (XSS)
    # ---------------------------------------------------------
    # If home.html uses {{ fname|safe }} or similar unsafe rendering,
    # an attacker could pass:
    # ?fname=<script>alert('Hacked')</script>
    # This would execute JavaScript in the victim's browser.
    # ---------------------------------------------------------
    


@app.route('/add_user', methods=['POST'])



def add_user():
    fname = request.form.get('fname')
    lname = request.form.get('lname')
    email = request.form.get('email')
    password = request.form.get('password')


    hashed_pw = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    connection = sqlite3.connect('LoginData.db')
    cursor = connection.cursor()


    ans = cursor.execute("SELECT * FROM USERS WHERE email = ?", (email,)).fetchall()

    if len(ans) > 0:
        connection.close()
        return render_template('login.html', error="User already exists")
    else:

        query = "INSERT INTO USERS(first_name, last_name, email, password) VALUES(?, ?, ?, ?)"
        cursor.execute(query, (fname, lname, email, hashed_pw))

        connection.commit()
        connection.close()

        return render_template('login.html')



@app.route('/redirect_me')
def redirect_me():

    # ---------------------------------------------------------
    # OPEN / INVALID REDIRECT
    # ---------------------------------------------------------
    # This blindly redirects to a user-supplied URL.
    # An attacker could craft:
    # /redirect_me?next=https://malicious-site.com
    # Victims trust the domain and get redirected to phishing site.
    # ---------------------------------------------------------
    next_url = request.args.get('next')
    return redirect(next_url)


@app.route('/download')
def download():

    # ---------------------------------------------------------
    # FILE ATTACK (Path Traversal)
    # ---------------------------------------------------------
    # User controls filename.
    # Attacker could request:
    # /download?file=../../../../etc/passwd
    # and retrieve sensitive server files.
    # ---------------------------------------------------------
    filename = request.args.get('file')
    return send_file(filename)


@app.route('/transfer_money', methods=['POST'])
def transfer_money():

    # ---------------------------------------------------------
    # CROSS-SITE REQUEST FORGERY (CSRF)
    # ---------------------------------------------------------
    # No CSRF token validation.
    # If a logged-in user visits a malicious site,
    # that site could auto-submit a form to this endpoint
    # and perform actions without the user's consent.
    # ---------------------------------------------------------

    amount = request.form.get('amount')
    recipient = request.form.get('recipient')

    return f"Transferred ${amount} to {recipient}"


if __name__ == '__main__':
    serve(app, host="0.0.0.0", port=8000)



#------------------------------------------------------
#PROBLEM LIST
#------------------------------------------------------
#SQL INJECTION-STATUS COMPLETE
#SESSION MANAGEMENT-STATUS COMPLETE
#SIDE CHANNEL ATTACK-STATUS COMPLETE
#------------------------------------------------------
