from __future__ import absolute_import, print_function, unicode_literals

import time
import sys
import datetime
from collections import defaultdict

from .settings import REQUESTS_PER_WINDOW, RATE_LIMIT_WINDOW, QUERIES, TWEETS_PER_REQUEST, RATE_DECAY
from .core import get_tweets_count_times, get_twitter, process_argv



def cron(queries):
    twitter = get_twitter()

    rounds = 0
    counts = defaultdict(int)
    rates = count_per_window(int)

    while True:
        rounds += 1

        start = time.time()
        # start out with all queries given the maximum rate allowed by the API
        tweet_rate = dict((k, TWEETS_PER_REQUEST * REQUESTS_PER_WINDOW * 1. / len(queries)) for k in queries)

        for query in queries:
            now = datetime.datetime.utcnow()
            print('Round {} started: {}'.format(rounds, now))

            num_tweets, rate_limit_remaining = get_tweets_count_times(twitter, count=2, query=query)

            now = time.time()
            if num_tweets < TWEETS_PER_REQUEST:
                rate = num_tweets * 1. / RATE_LIMIT_WINDOW  # this is a little slower than the truth, they'll keep coming in for the remainder 
                tweet_rate[query] = RATE_DECAY * tweet_rate[query] + (1 - RATE_DECAY) * rate

            stats[query] += num_tweets

        now = datetime.datetime.utcnow()
        print('Round {} finished: {}'.format(rounds, datetime.datetime.utcnow()))
        print()

        time.sleep(RATE_LIMIT_WINDOW - )


if __name__ == '__main__':
    queries, verbosity = process_argv(sys.argv)
    cron(queries=queries, verbosity=verbosity)
