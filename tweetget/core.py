from __future__ import absolute_import, print_function, unicode_literals
import os
import json
import datetime
import settings
from read import print_tweets

from twython import Twython

# When an application exceeds the rate limit for a given API endpoint, the Twitter API will now return an HTTP 429 “Too Many Requests” response code.
# If you hit the rate limit on a given endpoint, this is the body of the HTTP 429 message that you will see:
# { "errors": [ { "code": 88, "message": "Rate limit exceeded" } ] }


def _get(twitter, oldest_id=None):
    params = {
        'q': 'python -monty',
        'lang': 'en',
        'count': '100',
        'result_type': 'recent'
    }

    if oldest_id:
        params['max_id'] = oldest_id

    resp = twitter.search(**params)

    if False:  # toggle this to make the script more or less chatty
        print_tweets(resp['statuses'])

    return resp['statuses']


def _get_oldest_id():
    if not os.path.isfile(settings.OLDEST_ID_PATH):
        return None

    with open(settings.OLDEST_ID_PATH, 'r') as f:
        oldest_id = int(f.read())

    return oldest_id


def _set_oldest_id(oldest_id):
    with open(settings.OLDEST_ID_PATH, 'w') as f:
        f.write(str(oldest_id))

    return oldest_id


def get_tweets(twitter, request_count=settings.RATE_LIMIT):
    """ hits the twitter api :request_count: times and grabs tweets
    """
    # get id to start from
    oldest_id = _get_oldest_id()

    statuses = []
    i = 0
    while i < request_count:
        i += 1
        # get the actual tweets
        tweets = _get(twitter, oldest_id)
        statuses.extend(tweets)

        # determine new oldest id
        tweet_ids = {t['id'] for t in tweets}
        tweet_ids.add(oldest_id)
        oldest_id = min(tweet_ids)

    # store results in a file
    now = datetime.datetime.utcnow()
    filename = 'raw/{}.json'.format(now)
    with open(filename, 'a') as f:
        f.write(json.dumps(statuses, indent=2))

    # set id to start from for next time
    _set_oldest_id(oldest_id)


def get_twitter():
    twitter = Twython(settings.TWITTER_API_KEY, settings.TWITTER_API_SECRET, oauth_version=2)
    return Twython(settings.TWITTER_API_KEY, access_token=twitter.obtain_access_token())


if __name__ == '__main__':
    twitter = get_twitter()
    get_tweets(twitter)
