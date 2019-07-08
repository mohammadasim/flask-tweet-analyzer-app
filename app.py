from flask import Flask, render_template
from twitter_utils import get_request_token
import config

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)


def create_tables():
    db.create_all()


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    request_token = get_request_token()


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run()
    

