from flask import Flask, render_template, session, redirect, request
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
import config
from models.user import User

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)


@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    request_token = get_request_token()
    session['request_token'] = request_token
    return redirect(get_oauth_verifier_url(request_token))


@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.find_by_screen_name(access_token['screen_name'])
    if user is None:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'])
        user.save_to_db()
    session['screen_name'] = user.screen_name

    return user.screen_name



if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run()
    

