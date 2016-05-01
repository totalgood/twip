from __future__ import absolute_import, print_function, unicode_literals
import os
import json
import settings
import random


def print_tweets(tweets):
    for tweet in tweets:
        print('---------------------')
        print(tweet['created_at'])
        print(tweet['text'])

    print('--------------------')


def read(count):
    """ prints :count: random tweets
    """
    if not os.path.isfile(settings.MERGED_DATA_LOCATION):
        print('No data to read! Please run the merge script then run this!')

    with open(settings.MERGED_DATA_LOCATION, 'r') as f:
        tweets = json.loads(f.read())

    tweet_dict = {t['id']: t for t in tweets}
    random_ids = random.sample(tweet_dict.keys(), count)

    random_tweets = [tweet_dict[rid] for rid in random_ids]
    print_tweets(random_tweets)


if __name__ == '__main__':
    read(10)
