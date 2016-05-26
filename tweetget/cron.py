from __future__ import absolute_import, print_function, unicode_literals
import time
import datetime
from .settings import RATE_LIMIT, RATE_LIMIT_WINDOW
from .core import get_tweets_count_times, get_twitter


def cron():
    twitter = get_twitter()

    rounds = 0
    while True:
        rounds += 1

        now = datetime.datetime.utcnow()
        print('Round {} started: {}'.format(rounds, now))

        get_tweets_count_times(twitter, RATE_LIMIT)

        now = datetime.datetime.utcnow()
        print('Round {} finished: {}'.format(rounds, now))
        print()

        time.sleep(RATE_LIMIT_WINDOW + 60)


if __name__ == '__main__':
    cron()
