from database import db
from twitter_utils import consumer
import oauth2
import json


class User(db.Model):
    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String)
    first_name = db.Column(db.String)
    last_name = db.Column(db.String)
    oauth_token = db.Column(db.String)
    oauth_token_secret = db.Column(db.String)

    def __repr__(self):
        return "<User {}>".format(self.email)

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        query = db.session.query.filter_by(email=email).first()
        return query

    def make_a_request(self, url, verb,):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)
        response, content = authorized_client.request(url, verb)
        if response.status != 200:
            return {'message': 'An error has happened.', 'http_status_code received': response.status}
        else:
            return json.loads((content.decode('utf-8')))


