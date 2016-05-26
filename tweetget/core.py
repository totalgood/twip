# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import os

from .settings import OLDEST_ID_PATH, RATE_LIMIT
from .single import get_tweets, save_tweets, get_twitter


def _get_oldest_id():
    if not os.path.isfile(OLDEST_ID_PATH):
        return None

    with open(OLDEST_ID_PATH, 'r') as f:
        oldest_id = int(f.read())

    return oldest_id


def _set_oldest_id(oldest_id):
    with open(OLDEST_ID_PATH, 'w') as f:
        f.write(str(oldest_id))


def get_tweets_count_times(twitter, count):
    """ hits the twitter api :count: times and grabs tweets
    """
    # get id to start from
    oldest_id = _get_oldest_id()

    all_tweets = []
    i = 0
    while i < count:
        i += 1
        # get the actual tweets
        tweets = get_tweets(twitter, oldest_id)
        if not len(tweets):
            break

        all_tweets.extend(tweets)

        # determine new oldest id
        tweet_ids = {t['id'] for t in tweets}
        if oldest_id:
            tweet_ids.add(oldest_id)
        oldest_id = min(tweet_ids)

    save_tweets(all_tweets)

    # set id to start from for next time
    _set_oldest_id(oldest_id)


if __name__ == '__main__':
    twitter = get_twitter()
    get_tweets_count_times(twitter, RATE_LIMIT)
