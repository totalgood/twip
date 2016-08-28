from __future__ import absolute_import, print_function, unicode_literals

import time
import sys
import datetime

from .settings import RATE_LIMIT, RATE_LIMIT_WINDOW, QUERY
from .core import get_tweets_count_times, get_twitter



def cron(query=None):
    twitter = get_twitter()

    rounds = 0
    while True:
        rounds += 1

        now = datetime.datetime.utcnow()
        print('Round {} started: {}'.format(rounds, now))

        get_tweets_count_times(twitter=twitter, count=RATE_LIMIT, query=query)
	rate_limit_remaining = twitter.get_lastfunction_header('x-rate-limit-remaining')
	rate_limit_reset = twitter.get_lastfunction_header('x-rate-limit-reset')

        now = datetime.datetime.utcnow()
        print('Round {} finished: {}'.format(rounds, now))
        print('rate limit remaining: {}\nrate limit reset: {}'.format(rate_limit_remaining, rate_limit_reset))
        print()

        time.sleep(RATE_LIMIT_WINDOW + 60)


if __name__ == '__main__':
    query = QUERY
    if len(sys.argv) > 1:
        query = ' '.join(sys.argv[1:])
    cron(query=query)
