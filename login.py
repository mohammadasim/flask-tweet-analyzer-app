from user import User
import constants
import oauth2
import urllib.parse as urlparse
from twitter_utils import consumer, get_request_token


def create_authorized_user(email, first_name, last_name):
    request_token = get_request_token()
    print('Please click the following link to get a pin')
    print('{}?oauth_token={}'.format(constants.AUTHORIZATION_URL, request_token['oauth_token']))
    verified_pin  = input('Please enter the pin received from Tweeter:  ')
    token = oauth2.Token(request_token['oauth_token'], request_token['oauth_token_secret'])
    token.set_verifier(verified_pin)
    client = oauth2.Client(consumer, token)
    response, content = client.request(constants.ACCESS_TOKEN_URL, 'POST')
    access_token = dict(urlparse.parse_qsl(content.decode('utf-8')))
    user = User(email, first_name, last_name, access_token['oauth_token'], access_token['oauth_token_secret'])
    user.save_to_db()
    return user
