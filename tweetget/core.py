# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division
from builtins import str

import os
import sys

from .settings import DATA_PATH, TWEETS_PER_SEARCH, QUERIES
from .single import get_tweets, save_tweets, get_twitter


def make_oldest_id_path(query=''):
   return os.path.join(DATA_PATH, '--'.join([s for s in (query, 'oldest_id.txt') if s]))


def _get_oldest_id(query=''):
    oldest_id_path = make_oldest_id_path(query)

    if not os.path.isfile(oldest_id_path):
        return None

    with open(oldest_id_path) as f:
        oldest_id = int(f.read())

    return oldest_id


def _set_oldest_id(oldest_id, query=None):
    with open(make_oldest_id_path(query or ''), 'w') as f:
        f.write(str(oldest_id))


def get_tweets_count_times(twitter, count, query=None):
    r""" hits the twitter api `count` times and grabs tweets for the indicated query"""
    # get id to start from
    oldest_id = _get_oldest_id(query=query)

    all_tweets = []
    i = 0
    while i < count:
        i += 1
        # use search api to request 100 tweets. Twitter returns the most recent (max_id) first
        tweets = get_tweets(query=query, max_id=oldest_id - 1, count=TWEETS_PER_SEARCH, twitter=twitter)
        if not len(tweets):
            break

        all_tweets.extend(tweets)

        # determine new oldest id
        tweet_ids = {t['id'] for t in tweets}
        if oldest_id:
            tweet_ids.add(oldest_id)
        oldest_id = min(tweet_ids)

    save_tweets(all_tweets, query=query)

    # set id to start from for next time
    _set_oldest_id(oldest_id, query=query)

    if len(all_tweets) == 0:
        os.remove(make_oldest_id_path(query))

    return len(all_tweets), twitter.get_lastfunction_header('x-rate-limit-remaining')


def process_argv(argv):
    queries = QUERIES
    if len(argv) > 1:
        if '--verbose' in argv[1:]:
            argv = [a for a in argv if a != '--verbose']
            verbosity = 1 
        queries = argv[1:]
    return queries, verbosity 


if __name__ == '__main__':
    queries, verbosity = process_argv(sys.argv)
    twitter = get_twitter()
    for q in queries:
        get_tweets_count_times(query=q, twitter=twitter, verbosity=verbosity)
