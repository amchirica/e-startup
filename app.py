from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'xyzsdfg'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Quartz1983'
app.config['MYSQL_DB'] = 'estartup'
mysql = MySQL(app)

@app.route('/')
@app.route('/index.html')
def homeindex():
    return render_template('index.html')

@app.route('/blog.html')
def blog():
    return render_template('blog.html')

@app.route('/about.html')
def about():
    return render_template('about.html')


@app.route('/project.html')
def project():
    return render_template('project.html')

@app.route('/policy.html')
def policy():
    return render_template('policy.html')

@app.route('/contact.html')
def contact():
    return render_template('contact.html')

@app.route('/login.html', methods =['GET', 'POST'])
def login():
    mesage = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        username = request.form["username"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM clients WHERE email = % s AND password = % s', (email, password, ))
        client = cursor.fetchone()
        if client:
            session['loggedin'] = True
            session['userid'] = client['clientid']
            session['name'] = client['accountname']
            session['email'] = client['email']
            mesage = 'Logged in successfully !'
            #return render_template('user.html', mesage = mesage)
            print("asdasddas")
        else:
            mesage = 'Please enter correct email / password !'
    return render_template('login.html', mesage = mesage)

if __name__ == '__main__':
    app.run(debug=True)