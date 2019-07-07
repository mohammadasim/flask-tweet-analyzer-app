import os

CONSUMER_KEY = os.environ.get('CONSUMER_KEY_TWITTER')
CONSUMER_SECRET = os.environ.get('CONSUMER_SECRET_TWITTER')

REQUEST_TOKEN_URL = 'https://api.twitter.com/oauth/request_token'
ACCESS_TOKEN_URL = 'https://api.twitter.com/oauth/access_token'
AUTHORIZATION_URL = 'https://api.twitter.com/oauth/authorize'




