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
@app.route('/home')
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
        password = request.form['password']
        username = request.form["username"]
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM clients WHERE accountname = % s AND password = % s', (username, password, ))
        
        client = cursor.fetchone()
        if client:
            session['loggedin'] = True
            session['userid'] = client['clientid']
            session['name'] = client['accountname']
            session['email'] = client['email']
            return redirect('user')
        elif username == 'admin' and password == 'admin':
            session['loggedin'] = True
            session['userid'] = '0'
            session['name'] = 'admin'
            session['email'] = 'admin'
            return redirect('dashboard')
        else:
            mesage = 'Please enter correct email / password !'
    

    return render_template('login.html')


@app.route('/register',methods =['GET', 'POST'])
def register():
    if request.method == 'POST' and 'user_name' in request.form and 'user_password' in request.form and 'user_email' in request.form\
        and 'user_surname' in request.form and 'user_phone' in request.form and 'account_name' in request.form:
        name = request.form['user_name']
        surname = request.form['user_surname']
        account_name = request.form['account_name']
        email = request.form['user_email']
        phone = request.form['user_phone']
        password = request.form['user_password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        try:
            cursor.execute('insert into clients (employeeid,password,name,surname,email,phone,accountname) VALUES (% s, % s, % s, % s,% s, % s, % s)',\
                (None, password, name,surname,email,phone,account_name, ))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM clients WHERE accountname = % s AND password = % s', (account_name, password, ))
            client = cursor.fetchone()
            print(client)
            if client:
                session['loggedin'] = True
                session['userid'] = client['clientid']
                session['name'] = client['accountname']
                session['email'] = client['email']
                return redirect('user')
        except Exception:
            pass
        
    return render_template('register.html')


@app.route('/user', methods =['GET', 'POST'])
def user():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if request.method == 'POST':
        
        #introducere in tabela projects
        project = request.form['user_project']
        #phone = request.form['user_phone']
        budget = request.form['user_budget']
        try:
            technologyJava = request.form['Java+Spring']
        except Exception:
            pass
        try:
            technologyPython = request.form['Python+Flask']
        except Exception:
            pass
        try:
            technologyCsharp = request.form['C#+AspDotNet']
        except Exception:
            pass

        cursor.execute("insert into projects(clientid,name,cost) values(% s,% s,%s)",(int(session['userid']),project,float(budget),))
        mysql.connection.commit()
        
        #interogare tabela pentru a obtine idiul generat
        cursor.execute("select projectid from projects where name=%s",(project,))
        projectid = cursor.fetchone()
        print(projectid['projectid'])

        
        #introducere in tabela technologies
        try:
            cursor.execute("insert into technologies(projectid,name) values(% s,% s)",(projectid['projectid'],technologyJava,))
            mysql.connection.commit()        
        except Exception:
            pass
        try:
            cursor.execute("insert into technologies(projectid,name) values(% s,% s)",(projectid['projectid'],technologyPython,))
            mysql.connection.commit()        
        except Exception:
            pass
        try:
            cursor.execute("insert into technologies(projectid,name) values(% s,% s)",(projectid['projectid'],technologyCsharp,))
            mysql.connection.commit()        
        except Exception:
            pass


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
    return redirect('login')

@app.route('/dashboard',methods =['GET', 'POST'])
def dashboard():
    
    
    if session['name'] == 'admin':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from employee")
        employee = cursor.fetchall()
    
        cursor.execute("select * from clients")
        clients = cursor.fetchall()
        
        if request.method == 'POST' and 'name' in request.form:
            name_employee = request.form['name']
            surname_employee = request.form['surname']
            budget_employee = request.form['budget']
            cursor.execute("insert into employee(name,surname,budget) values(%s,%s,%s);", (name_employee,surname_employee,budget_employee,))
            mysql.connection.commit()
        sql_statement = "UPDATE clients\
                        SET employeeid = %s\
                        WHERE clientid = %s;"
        for client in clients:
            if request.method == 'POST' and str(client['clientid']) in request.form:
                if request.form[str(client['clientid'])] != "":
                    try:
                        cursor.execute(sql_statement, (request.form[str(client['clientid'])],client['clientid'],))
                        mysql.connection.commit()
                    except Exception:
                        pass
        cursor.execute("select * from employee")
        employee = cursor.fetchall()
        
        cursor.execute("select * from clients")
        clients = cursor.fetchall()
        
        #data for org structure
        org_structure = {}
        cursor.execute("select count(employeeid) employees_number from employee")
        employee_number = cursor.fetchone()
        org_structure.update(employee_number)
        
        cursor.execute("select count(clientid) clients_number from clients")
        clients_number = cursor.fetchone()
        org_structure.update(clients_number)
        
        cursor.execute("select count(projectid) projects_number from projects")
        projects_number = cursor.fetchone()
        org_structure.update(projects_number)
        
        cursor.execute("select cast(sum(budget) as signed) total_budget from employee")
        total_budget = cursor.fetchone()
        org_structure.update(total_budget)
        
        cursor.execute("select cast(sum(cost) as signed) total_cost from projects")
        total_cost = cursor.fetchone()
        org_structure.update(total_cost)
        
        
        print(org_structure)
        return render_template('dashboard.html',employee = employee,clients = clients, org_structure = org_structure)

@app.route('/widget')
def widget():
    return render_template('widget.html')

@app.route('/chart')
def chart():
    return render_template('chart.html')

@app.route('/table')
def table():
    
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute("select * from clients")
    clients = cursor.fetchall()

    cursor.execute("select * from employee")
    employees = cursor.fetchall()
    
    cursor.execute("select * from projects")
    projects = cursor.fetchall()
    
    cursor.execute("select * from technologies")
    technologies = cursor.fetchall()
    
    inner_join_statement =\
        "select\
            e.surname,\
            c.accountname,\
            p.name,\
            p.cost,\
            t.name\
        from employee e\
        inner join\
        clients c on(e.employeeid = c.employeeid)\
        inner join\
        projects p on(c.clientid = p.clientid)\
        inner join\
        technologies t on(t.projectid = p.projectid);"
    cursor.execute(inner_join_statement)
    inner_join_db = cursor.fetchall()

    return render_template('table.html', clients = clients, employees = employees, inner_join_db = inner_join_db,projects=projects,technologies = technologies)

if __name__ == '__main__':
    app.run(debug=True)