from pymongo import MongoClient
from bson import json_util
import json


class ExternalDataProvider:
    def __init__(self):
        self.MONGODB_URL = "mongodb://localhost:27017"
        self.client = MongoClient(self.MONGODB_URL)
        self.tweets_collection = self.client.dbms_project.tweets

    def get_tweets_by_user(self, query, page=1, per_page=10):
        """
        Search user by username and screen name, return json data
        :param page:
        :param per_page:
        :param query: username or screen name
        :return: list of dict, contain 'name', 'screenName', 'description', 'link'
        """

        start = (page - 1) * per_page
        results = self.tweets_collection.aggregate([
            {'$match': {'user.screen_name': query}},
            {'$skip': start},
            {'$limit': per_page},
            {'$project': {
                'tweet_id': {'$toString': '$tweet_id'},
                'text': 1,
                'user': 1,
                'created_at': 1
            }}
        ])

        return json.loads(json_util.dumps(list(results)))

    def get_tweets_by_text(self, query, page=1, per_page=10):
        """
        :param page: page number
        :param per_page: items per page
        :param query: keywords in text
        :return: list of dict, contains 'name', 'screenName', 'content', 'timestamp'
        """

        start = (page - 1) * per_page
        results = self.tweets_collection.aggregate([
            {'$match': {"$text": {"$search": query}}},
            {'$skip': start},
            {'$limit': per_page},
            {'$project': {
                'tweet_id': {'$toString': '$tweet_id'},
                'text': 1,
                'user': 1,
                'created_at': 1
            }}
        ])
        return json.loads(json_util.dumps(list(results)))

    def get_tweets_by_hashtag(self, query, page=1, per_page=10):
        """
        Search tweets by hashtag, return json data
        :param query: hashtag without #
        :param page: page number
        :param per_page: items per page
        :return: list of dict
        """

        start = (page - 1) * per_page
        results = self.tweets_collection.aggregate([
            {'$match': {"hashtags": query}},
            {'$skip': start},
            {'$limit': per_page},
            {'$project': {
                'tweet_id': {'$toString': '$tweet_id'},
                'text': 1,
                'user': 1,
                'created_at': 1
            }}
        ])

        return json.loads(json_util.dumps(list(results)))


data_provider = ExternalDataProvider()
