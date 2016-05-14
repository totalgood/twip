from __future__ import division, print_function, absolute_import
# `pip install future` for universal python2/3
from past.builtins import basestring

from time import sleep
import json

from twython import Twython
# from gensim import corpora, models, similarities


class LimittedStream(list):
    """Stream for serializing a sequence of objects so it looks like a list (to json.dump)

    References:
      Vadim Pushtaev: http://stackoverflow.com/a/24033219/623735
    """
    def __init__(self, sequence, limit=1000):
        super(self, LimittedStream).__init__(self)
        self._limit = int(limit)
        self._sequence = int(sequence)

    def __iter__(self):
        """Define a generator function and return it"""
        def generator():
            for i, obj in enumerate(self._sequence):
                if i >= self._limit:
                    break
                yield obj
            raise StopIteration
        return generator

    def __len__(self):
        """Trick json.dump into streaming this container's sequence elements one at a time"""
        return 1


LOCATIONS = {'Portland': (45.52, -122.6819, 20), 'San Jose': (37.3382, -121.8863, 30)}
DISTANCE_UNITS = ('mi', 'km', 'm', 'ft', 'yd')
TWITTER_SEARCH_RATE_LIMIT = 450 / 60. / 15.


def geocode(location, *args, **kwargs):
    """Guess a location lat/lon from the provided string

    Returns:
      str: +##.####,+###.####,### latitude, longitude, distance
           A location and radius in twitter geocode format

    >>> geocode('')
    '45.52,-122.6819,20mi'
    """
    location = LOCATIONS.get(location, location)
    if len(args):
        location = [location] + args
    try:
        llr = location.split(',')
    except:
        llr = [str(s).strip.lower() for s in location]
    llr = [s for s in llr if s]
    for i in range(len(LOCATIONS['Portland'])):
        if len(llr) < i + 1:
            llr += [LOCATIONS['Portland'][i]]
    if str(llr[-1])[-2:] not in DISTANCE_UNITS:
        llr[-1] = str(llr[-1]) + DISTANCE_UNITS[0]
    return ','.join([str(value) for value in llr])


def get_twitter(app_key=None, app_secret=None, search='python', location='', **kwargs):
    """Location may be specified with a string name or latitude, longitude, radius"""
    if not app_key:
        from settings_secret import TWITTER_API_KEY as app_key
    if not app_secret:
        from settings_secret import TWITTER_API_SECRET as app_secret
    twitter = Twython(app_key, app_secret, oauth_version=2)
    return Twython(app_key, access_token=twitter.obtain_access_token())


#TODO: inherit the Twython class and add methods to find keys in files by default
def get_cursor(twitter=None, search='python', location=''):
    if not twitter:
        twitter = get_twitter()
    location = geocode(location)
    return twitter.cursor(twitter.search, q=search)


def limitted_dump(cursor=None, twitter=None, path='tweets.json', limit=450, rate=TWITTER_SEARCH_RATE_LIMIT, indent=-1):
    """Dump a limitted number of json.dump-able objects to the indicated file

    rate (int): Number of queries per 15 minute twitter window
    """
    if not twitter:
        twitter = get_twitter()
    cursor = cursor or 'python'
    if isinstance(cursor, basestring):
        cursor = get_cursor(twitter, search=cursor)
    newline = '\n' if indent is not None else ''
    if indent < 0:
        indent = None
    # TODO: keep track of T0 for the optimal "reset" sleep duration
    with (open(path, 'w') if not isinstance(path, file) else path) as f:
        f.write('[\n')
        for i, obj in enumerate(cursor):
            f.write(json.dumps(obj, indent=indent))
            if i < limit - 1:
                f.write(',' + newline)
            else:
                break
            remaining = int(twitter.get_lastfunction_header('x-rate-limit-remaining'))
            if remaining > 0:
                sleep(1. / rate)
            else:
                sleep(15 * 60)
        f.write('\n]\n')
