import lib.Settings as s
from requests_oauthlib import OAuth1Session

config = s.Settings('twitter.json')


class Twitter:
    def __init__(self):
        # Access Credentials
        self.consumer_key = config.get("consumer_key")
        self.consumer_secret = config.get("consumer_secret")
        self.access_token = config.get("access_token")
        self.access_secret = config.get("access_secret")

        self.base_url = config.get("base_url")

        self.query = None

    def set_query(self, query):
        self.query = query

    def query(self):
        query = self.base_url + self.query
        oauth = OAuth1Session(self.consumer_key,
                              client_secret=self.consumer_secret,
                              resource_owner_key=self.access_token,
                              resource_owner_secret=self.access_secret)

        params = {}

        return oauth.get(query, params=params).json()
