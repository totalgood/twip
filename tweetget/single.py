import json
import datetime
from twython import Twython
from .settings import DATA_DIR, TWITTER_API_KEY, TWITTER_API_SECRET

QUERY = 'python -monty'


def get_twitter():
    twitter = Twython(TWITTER_API_KEY, TWITTER_API_SECRET, oauth_version=2)
    return Twython(TWITTER_API_KEY, access_token=twitter.obtain_access_token())


def get_tweets(twitter, oldest_id=None):
    params = {
        'q': QUERY,
        'lang': 'en',
        'count': '100',
        'result_type': 'recent'
    }

    if oldest_id:
        params['max_id'] = oldest_id

    resp = twitter.search(**params)

    return resp['statuses']


def save_tweets(tweets):
    now = datetime.datetime.utcnow()
    filename = '{}{}.json'.format(DATA_DIR, now.isoformat())
    with open(filename, 'a') as f:
        f.write(json.dumps(tweets, indent=2))

    print('tweets written to {}'.format(filename))


if __name__ == '__main__':
    twitter = get_twitter()
    tweets = get_tweets(twitter)
    save_tweets(tweets)
