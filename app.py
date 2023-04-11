from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re

app = Flask(__name__)

app.secret_key = 'xyzsdfgqadasdads'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Quartz1983'
app.config['MYSQL_DB'] = 'estartup'
mysql = MySQL(app)

@app.route('/')
@app.route('/index')
def homeindex():
    return render_template('index.html')

@app.route('/blog')
def blog():
    return render_template('blog.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.route('/project')
def project():
    return render_template('project.html')

@app.route('/policy')
def policy():
    return render_template('policy.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/login', methods =['GET', 'POST'])
def login():

    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        username = request.form["username"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        #cursorOrg = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM clients WHERE accountname = % s AND password = % s', (username, password, ))
        #cursorOrg.execute('SELECT * FROM clients WHERE email = % s AND password = % s', (username, password, ))
        print(password == 'admin')
        print(username == 'admin')
        client = cursor.fetchone()
        if client:
            session['loggedin'] = True
            session['userid'] = client['clientid']
            session['name'] = client['accountname']
            session['email'] = client['email']
            mesage = 'Logged in successfully !'
            return redirect('user')
        elif username == 'admin' and password == 'admin':
            return render_template('blog.html')
        else:
            mesage = 'Please enter correct email / password !'
    
    if session.get("name"):
        return redirect('user')
    else:
        return render_template('login.html')


@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/user', methods =['GET', 'POST'])
def user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        
        #introducere in tabela projects
        project = request.form['user_project']
        phone = request.form['user_phone']
        budget = request.form['user_budget']
        technology = request.form['user_tehnology']
        cursor.execute("insert into projects(clientid,name,cost) values(% s,% s,%s)",(int(session['userid']),project,float(budget),))
        mysql.connection.commit()
        
        #interogare tabela pentru a obtine idiul generat
        cursor.execute("select projectid from projects where name=%s",(project,))
        projectid = cursor.fetchall()
        print(projectid[0]['projectid'])

        
        #introducere in tabela technologies
        cursor.execute("insert into technologies(projectid,name) values(% s,% s)",(projectid[0]['projectid'],technology,))
        mysql.connection.commit()

        #interogare tabela client, project, technologies
    sql_statement = "select\
            p.name,\
            p.cost,\
            t.name\
        from clients c inner join \
        projects p on(c.clientid = p.clientid)\
        inner join \
        technologies t on(t.projectid = p.projectid)\
        where c.clientid = % s;"
    cursor.execute(sql_statement,(session['userid'],))
    client_info = cursor.fetchall()
    print(client_info)
    return render_template('user.html',message = client_info)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    session.pop('name', None)
    return redirect('login.html')

if __name__ == '__main__':
    app.run(debug=True)