import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

# $ export FLASK_ENV=development
# $ flask run

@app.route('/')
def index():
    return render_template('index.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/work')
def work():
    return render_template('work.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/hobbies')
def hobbies():
    return render_template('hobbies.html', title="MLH Fellow", url=os.getenv("URL"))

@app.route('/places')
def places():
    return render_template('places.html', title="MLH Fellow", url=os.getenv("URL"))
