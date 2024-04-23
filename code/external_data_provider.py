import search


class ExternalDataProvider:
    # TODO replace data source of all functions by database data
    # def __init__(self):
    #     self.searcher = search.Searcher()

    def get_user(self, query):
        """
        Search user by username and screen name, return json data
        :param query: username or screen name
        :return: list of dict, contain 'name', 'screenName', 'description', 'link'
        """
        # TODO maybe we need to search twice and combine them together, up to you
        name_data, screenName_data = [], []
        data = name_data + screenName_data

        demo_data = [
            {'name': 'Alice', 'description': 'Loves cats and coffee.', 'link': 'https://twitter.com/CNN'},
            {'name': 'Bob', 'description': 'Avid hiker and photographer.', 'link': 'https://twitter.com/elonmusk'},

        ]

        return demo_data[:10]

    def get_tweets_by_text(self, query, page=1, per_page=10):
        """
        :param page: page number
        :param per_page: items per page
        :param query: keywords in text
        :return: list of dict, contains 'name', 'screenName', 'content', 'timestamp'
        """
        # TODO try use limit & offset to separate by page
        start = (page - 1) * per_page
        end = start + per_page
        # result = self.db.execute(
        #     "SELECT * FROM tweets WHERE content LIKE :query LIMIT :limit OFFSET :offset",
        #     {'query': f'%{query}%', 'limit': per_page, 'offset': offset}
        # )
        demo_data = [
            {'user': 'Alice', 'content': 'Just had the best coffee ever!', 'timestamp': '2024-04-20T08:30:00',
             'link': 'https://twitter.com/CNN/status/1782795635181187356'},
            {'user': 'Bob', 'content': 'A beautiful day in the mountains.', 'timestamp': '2024-04-20T09:00:00',
             'link': 'https://twitter.com/elonmusk/status/1782550334155420074'},

        ]
        demo_data = (demo_data * 25)[start:end]

        return demo_data

    def get_tweets_by_hashtag(self, query, page=1, per_page=10):
        """
        Search tweets by hashtag, return json data
        :param query: hashtag without #
        :param page: page number
        :param per_page: items per page
        :return: list of dict
        """
        start = (page - 1) * per_page
        end = start + per_page
        # Simulated data; replace with database query
        demo_data = [
            {'user': 'Alice', 'content': '#love this cafe!', 'timestamp': '2024-04-20T08:30:00',
             'link': 'https://twitter.com/CNN/status/1782795635181187356'},
            {'user': 'Bob', 'content': '#hiking rocks!', 'timestamp': '2024-04-20T09:00:00',
             'link': 'https://twitter.com/elonmusk/status/1782550334155420074'},
        ]
        return (demo_data * 25)[start:end]


data_provider = ExternalDataProvider()
