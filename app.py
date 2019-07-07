from flask import Flask, render_template
from twitter_utils import get_request_token
import os

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = 'postgresql://{username}:{password}@localhost/{database}'.\
    format(username=os.environ.get('PSQL_USER'), password=os.environ.get('PSQL_USER_PASSWORD'),
           database=os.environ.get('PSQL_DB_NAME'))


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    request_token = get_request_token()
    

