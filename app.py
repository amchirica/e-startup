from flask import Flask, render_template
import os
from forms import RegistrationForm, LoginForm

app = Flask(__name__)

app.config['SECRET_KEY'] = 'hdaLSDHAILSDHADKLA129412748'

img = os.path.join('static', 'img')


@app.route('/')
@app.route('/index.html')
def homeindex():
    return render_template('index.html')

@app.route('/blogslist.html')
def blogslist():
    return render_template('blogslist.html')

@app.route('/blog.html')
def blogspot():
    return render_template('blog.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

app.route('/login.html')
def login():
    return render_template('login.html')

app.route('/project.html')
def project():
    return render_template('project.html')

app.route('/policy.html')
def policy():
    return render_template('policy.html')

app.route('/contact.html')
def contact():
    return render_template('contact.html')

app.route("/register")
def register():
    form = RegistrationForm()
    return render_template('register.html', title = 'Register', form = form)

app.route("/login")
def register():
    form = LoginForm()
    return render_template('login.html', title = 'Login', form = form)

if __name__ == '__main__':
    app.run(debug=True)