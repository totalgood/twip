# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals, division
# from builtins import str  # noqa

import os
import sys

from .settings import DATA_PATH, TWEETS_PER_SEARCH, QUERIES
from .single import get_tweets, save_tweets, get_twitter


def make_oldest_id_path(query=''):
    return os.path.join(DATA_PATH, '--'.join([s for s in (query, 'oldest_id.txt') if s]))


def _get_oldest_id(query=''):
    oldest_id_path = make_oldest_id_path(query)

    if not os.path.isfile(oldest_id_path):
        return None, None

    with open(oldest_id_path) as f:
        tokens = f.read().split()
    tokens = [tok.strip() for tok in tokens if len(tok.strip())]
    oldest_id = int(tokens[0])
    newest_id = int(tokens[1]) if len(tokens) > 1 else None

    return oldest_id, newest_id


def _set_oldest_id(oldest_id, newest_id, query=''):
    prev_oldest_id, prev_newest_id = _get_oldest_id(query=query)
    newest_id = max(newest_id, prev_newest_id or newest_id)
    with open(make_oldest_id_path(query), 'w') as f:
        if oldest_id < newest_id:
            f.write('{}\n{}\n', format(oldest_id, newest_id))
        else:
            f.write('{}\n{}\n', format(oldest_id, prev_newest_id))


def get_tweets_count_times(twitter, count, query=None):
    r""" hits the twitter api `count` times and grabs tweets for the indicated query"""
    # get id to start from
    oldest_id, newest_id = _get_oldest_id(query=query)
    newest_id = newest_id or oldest_id

    all_tweets = []
    i = 0
    while i < count:
        i += 1
        # use search api to request 100 tweets. Twitter returns the most recent (max_id) first
        if oldest_id <= newest_id:
            tweets = get_tweets(query=query, max_id=oldest_id - 1, count=TWEETS_PER_SEARCH, twitter=twitter)
        else:
            tweets = get_tweets(query=query, max_id=oldest_id - 1, since_id=newest_id, count=TWEETS_PER_SEARCH, twitter=twitter)
        rate_limit_remaining = twitter.get_lastfunction_header('x-rate-limit-remaining')
        rate_limit_reset = twitter.get_lastfunction_header('x-rate-limit-reset')

        if not len(tweets):
            # not rate limitted, just no tweets returned by query
            oldest_id = oldest_id + ((newest_id or oldest_id) - oldest_id + 1) * 10000
            break
        elif isinstance(tweets, dict):
            # rate limit hit, or other twython response error
            print(tweets)
            break

        all_tweets.extend(tweets)

        # determine new oldest id
        tweet_ids = {t['id'] for t in tweets}
        if oldest_id:
            tweet_ids.add(oldest_id)
        oldest_id, newest_id = min(tweet_ids), max(tweet_ids)
        if rate_limit_remaining == 1:
            time.sleep(rate_limit_reset)

    save_tweets(all_tweets, query=query)

    # set id to start from for next time
    _set_oldest_id(oldest_id, newest_id, query=query)

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
