from database import session_factory
from sqlalchemy import Column, Integer, String
from database import Base
from twitter_utils import consumer
import oauth2
import json


class User(Base):
    def __init__(self, email, first_name, last_name, oauth_token, oauth_token_secret):
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.oauth_token = oauth_token
        self.oauth_token_secret = oauth_token_secret

    __tablename__ = 'users'
    id = Column(Integer, primary_key=True)
    email = Column(String)
    first_name = Column(String)
    last_name = Column(String)
    oauth_token = Column(String)
    oauth_token_secret = Column(String)

    def __repr__(self):
        return "<User {}>".format(self.email)

    def save_to_db(self):
        session = session_factory()
        session.add(self)
        session.commit()

    @classmethod
    def find_by_email(cls, email):
        session = session_factory()
        query = session.query(User).filter_by(email=email).first()
        return query

    def make_a_request(self, url, verb,):
        authorized_token = oauth2.Token(self.oauth_token, self.oauth_token_secret)
        authorized_client = oauth2.Client(consumer, authorized_token)
        response, content = authorized_client.request(url, verb)
        if response.status != 200:
            return {'message': 'An error has happened.', 'http_status_code received': response.status}
        else:
            return json.loads((content.decode('utf-8')))


