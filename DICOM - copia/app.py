#import typing_extensions
from flask import Flask, render_template, request, redirect, url_for, session, flash
from flaskext.mysql import MySQL
import re

from pymysql import connect

app = Flask(__name__)

# Change this to your secret key (can be anything, it's for extra protection)
app.secret_key = 'your secret key'

# Enter your database connection details below
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_DB'] = 'dicom'
app.config['MYSQL_DATABASE_PORT'] = 3306

# Intialize MySQL
mysql = MySQL()
mysql.init_app(app)

print(mysql)

@app.route('/')
def begin():
    return render_template('begin.html')

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Output message if something goes wrong...
    msg = ''
        # Check if "username" and "password" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']

                # Check if account exists using MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        conn.commit()
        # Fetch one record and return result
        account = cursor.fetchone()
        print(account)
                # If account exists in accounts table in out database
        if account:
            # Create session data, we can access this data in other routes
            session['loggedin'] = True
            session['id'] = account[0]
            session['username'] = account[1]
            # Redirect to home page
            if session['id']==1 and session['username']=='test':
                return redirect(url_for('administrator'))
            else:
                return redirect(url_for('home'))
        else:
            # Account doesnt exist or username/password incorrect
            msg = 'Incorrect username/password!'

    return render_template('index.html', msg='')

    

    # http://localhost:5000/pythinlogin/register - this will be the registration page, we need to use both GET and POST requests
@app.route('/register', methods=['GET', 'POST'])
def register():
    # Output message if something goes wrong...
    msg = ''
    # Check if "username", "password" and "email" POST requests exist (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        # Create variables for easy access
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
                # Check if account exists using MySQL
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE username = %s AND password = %s', (username, password,))
        cursor.execute('SELECT * FROM accounts WHERE username = %s', (username,))
        conn.commit()
        account = cursor.fetchone()
        # If account exists show error and validation checks
        if account:
            msg = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address!'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers!'
        elif not username or not password or not email:
            msg = 'Please fill out the form!'
        else:
            # Account doesnt exists and the form data is valid, now insert new account into accounts table
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s, %s, %s)', (username, password, email,))
            conn.commit()
            msg = 'Registro Exitoso!' 
            return redirect(url_for('administrator'))
    elif request.method == 'POST':
        # Form is empty... (no POST data)
        msg = 'Please fill out the form!'
    # Show registration form with message (if any)
    return render_template('register.html', msg=msg)

    # http://localhost:5000/pythinlogin/home - this will be the home page, only accessible for loggedin users
@app.route('/home', methods = ['GET', 'POST'])
def home():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('home.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/administrator')
def administrator():
    # Check if user is loggedin
    if 'loggedin' in session:
        # User is loggedin show them the home page
        return render_template('administrator.html', username=session['username'])
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))

@app.route('/users')
def users():
    if 'loggedin' in session:
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts')
        conn.commit()
        usuarios = cursor.fetchall()
        usuarios=list(usuarios)
        for i in usuarios:
            if i[1]=="test":
                usuarios.remove(i)

        return render_template('users.html', usuarios=usuarios)
    
    return redirect(url_for('login'))

@app.route('/profile_admin')
def profile_admin():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile_admin.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/pythonlogin/logout')
def logout():
    # Remove session data, this will log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/profile')
def profile():
    # Check if user is loggedin
    if 'loggedin' in session:
        # We need all the account info for the user so we can display it on the profile page
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM accounts WHERE id = %s', (session['id'],))
        account = cursor.fetchone()
        # Show the profile page with account info
        return render_template('profile.html', account=account)
    # User is not loggedin redirect to login page
    return redirect(url_for('login'))


@app.route('/delete/<string:id>')
def delete_contact(id):
    conn = mysql.connect()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM accounts WHERE id = {0}'.format(id))
    conn.commit()
    usuarios = cursor.fetchall()
    flash('Contact Removed Succesfully!')
    return redirect(url_for('users'))    

@app.route('/edit/<id>')
def edit(id):
    cur = mysql.connect().cursor()
    cur.execute('SELECT * FROM accounts WHERE id = %s',(id))
    mysql.connect().commit()
    data = cur.fetchone()
    return render_template('edit_users.html', i = data)


@app.route('/update/<id>', methods = ['POST'])
def update(id):
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        conn = mysql.connect()
        cursor = conn.cursor()
        cursor.execute('UPDATE accounts SET username = %s, password = %s,email = %s WHERE id = %s', (username, password,email,id))
        conn.commit()
        flash('Account update Succesfully')
        return redirect(url_for('users'))

if __name__ == '__main__':
    app.run(debug=True)