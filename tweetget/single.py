# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function
from builtins import str

import json
import os
import datetime
import gzip
import sys

from twython import Twython
from .settings import DATA_PATH, TWITTER_API_KEY, TWITTER_API_SECRET, TWEETS_PER_REQUEST
from .core import process_argv


def get_twitter():
    twitter = Twython(TWITTER_API_KEY, TWITTER_API_SECRET, oauth_version=2)
    return Twython(TWITTER_API_KEY, access_token=twitter.obtain_access_token())


def get_tweets(query, count=TWEETS_PER_REQUEST, lang='en', result_type='recent', twitter=None, **kwargs):
    query = query
    twitter = twitter or get_twitter()

    params = {
        'q': query,
        'lang': lang,
        'count': str(int(count)),
        'result_type': result_type,
    }
    params.update(kwargs)

    # twython.exceptions.TwythonError: ('Connection aborted.', error(104, 'Connection reset by peer'))
    resp = twitter.search(**params)

    return resp['statuses']


def save_tweets(tweets, query='', verbosity=1):
    now = datetime.datetime.utcnow()
    filename = os.path.join(DATA_PATH, '{}-{}.json.gz'.format(query, now.isoformat()).replace(':', '_'))
    with gzip.open(filename, 'a') as f:
        f.write(json.dumps(tweets, indent=2))
    if verbosity > 0:
        print('{} tweets written to {}'.format(len(tweets), filename))


if __name__ == '__main__':
    args = process_argv(sys.argv)
    twitter = get_twitter()
    for q in args.queries:
        tweets = get_tweets(query=q, twitter=twitter)
        save_tweets(tweets)
