from flask import Flask, render_template, session, redirect, request, url_for, g
from forms.tweet_search_form import TweetSearchForm
from twitter_utils import get_request_token, get_oauth_verifier_url, get_access_token
import config
from models.user import User
import requests

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


@app.route('/auth/twitter') # Twitter redirects to this url
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


@app.route('/search/twitter', methods = ['POST', 'GET'])
def tweet_search():
    form = TweetSearchForm(request.form)
    if request.method == 'POST' and form.validate():
        session['searched_value'] = request.form['search']
        return redirect(url_for('tweet_search_results'))
    return render_template('search.html', form=form)


@app.route('/result', methods = ['POST','GET'])
def tweet_search_results():
    results = g.user.make_a_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.
                                    format(session['searched_value']), 'GET')
    return render_template('result.html', results=results)


@app.route('/search')# Method to seach using query string in the url /search?q=<search-item>
def search():
    query = request.args.get('q')
    tweets = g.user.make_a_request('https://api.twitter.com/1.1/search/tweets.json?q={}'.
                                    format(query), 'GET')
    tweet_texts = [{'tweet': tweet['text'], 'label': 'neutral'} for tweet in tweets['statuses']]

    for tweet in tweet_texts:
        r = requests.post('http://text-processing.com/api/sentiment/',data={'text': tweet['tweet']})
        json_response = r.json()
        label = json_response['label']
        tweet['label'] = label
    return render_template('results.html', content=tweet_texts)


if __name__ == '__main__':
    from database import db
    db.init_app(app)
    app.run()
    

