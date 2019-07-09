from flask import Flask, render_template, session, redirect, request, url_for, g
from forms.tweet_search_form import TweetSearchForm
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
import config
from models.user import User

app = Flask(__name__)
app.config.from_object(config.DevelopmentConfig)


@app.before_first_request
def create_tables():
    db.create_all()


@app.before_request
def load_user():
    if 'screen_name' in session:
        g.user = User.find_by_screen_name(session['screen_name'])


@app.route('/')
def homepage():
    return render_template('home.html')


@app.route('/login/twitter')
def twitter_login():
    if 'screen_name' in session:
        return redirect(url_for('profile'))
    else:
        request_token = get_request_token()
        session['request_token'] = request_token
        return redirect(get_oauth_verifier_url(request_token))


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('homepage'))


@app.route('/auth/twitter')
def twitter_auth():
    oauth_verifier = request.args.get('oauth_verifier')
    access_token = get_access_token(session['request_token'], oauth_verifier)

    user = User.find_by_screen_name(access_token['screen_name'])
    if user is None:
        user = User(access_token['screen_name'], access_token['oauth_token'], access_token['oauth_token_secret'])
        user.save_to_db()
    session['screen_name'] = user.screen_name

    return redirect(url_for('profile')) # redirected to the profile function, not the url


@app.route('/profile')
def profile():
    return render_template('profile.html', user=g.user) # We are passing a variable that will be accessed in the html page using jinja2 template


@app.route('/tweet/search', methods = ['POST', 'GET'])
def tweet_search():
    form = TweetSearchForm()
    print('I am stuck here')
    if request.method == 'POST':
        print('method is post')
        print(request)
        print(request.form['search'])
        session['searched_value'] = request.form['search']
        print('going to run redirect')
        return redirect(url_for('tweet_search_results'))
    return render_template('search.html', form=form)


@app.route('/result', methods = ['POST','GET'])
def tweet_search_results():
    print(session['searched_value'])
    return 'I have come to the search result section'


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run()
    

