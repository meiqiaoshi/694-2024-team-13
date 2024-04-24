from flask import Flask, render_template, request, jsonify
from external_data_provider import ExternalDataProvider

app = Flask(__name__)


@app.route('/')
def index():
    return render_template('home.html')


data_provider = ExternalDataProvider()


@app.route('/search', methods=['POST', 'GET'])
def search():
    page = int(request.args.get('page', 1))
    per_page = int(request.args.get('pageSize', 10))
    people = []
    if request.method == 'POST':
        query = request.form.get('query', '')
    else:
        query = request.args.get('query', '')

    if not query:  # empty query
        return jsonify({})

    if query.startswith('#'):  # search by hashtag
        query = query.lstrip('#')
        tweets = data_provider.get_tweets_by_hashtag(query, page, per_page)
    elif query.startswith('@'):  # search by user
        query = query.lstrip('@')
        tweets = data_provider.get_tweets_by_user(query, page, per_page)
    else:  # search by text
        tweets = data_provider.get_tweets_by_text(query, page, per_page)

    return jsonify(people=people, tweets=tweets)


@app.route('/search_user_tweets', methods=['GET'])
def search_user_tweets():
    username = request.args.get('username')
    if username:
        tweets = data_provider.get_tweets_by_user(username)  # 假设这个方法按用户名获取推文
        return jsonify(tweets=tweets)
    return jsonify({'error': 'Username not provided'}), 400


if __name__ == '__main__':
    app.run(debug=True, port=5000)
