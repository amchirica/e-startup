from flask import Flask, render_template
import os

app = Flask(__name__)

img = os.path.join('static', 'img')

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/index.html')
def homeindex():
    return render_template('index.html')

@app.route('/blogslist.html')
def blogslist():
    return render_template('blogslist.html')

@app.route('/blogpost.html')
def blogspot():
    return render_template('blogpost.html')

@app.route('/about.html')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)