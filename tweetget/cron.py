from __future__ import absolute_import, print_function, unicode_literals
import time
import datetime
import settings
from core import get_tweets, get_twitter


def cron():
    twitter = get_twitter()

    rounds = 0
    while True:
        rounds += 1

        now = datetime.datetime.utcnow()
        print('Round {} started: {}'.format(rounds, now))
        get_tweets(twitter)
        now = datetime.datetime.utcnow()
        print('Round {} finished: {}'.format(rounds, now))
        print()

        time.sleep(settings.RATE_LIMIT_WINDOW + 60)


if __name__ == '__main__':
    cron()
