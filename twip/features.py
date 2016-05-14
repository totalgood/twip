from __future__ import division, print_function, absolute_import
# `pip install future` for universal python2/3
from past.builtins import basestring

import os
import json
from zipfile import ZipFile

DATA_PATH = os.path.join('..', 'data')


def get_nested(obj, path):
    if isinstance(path, basestring):
        path = [path]
    if path:
        return get_nested(obj.get(path[0], {}), path[1:])
    else:
        return obj


def load_tweets(filename='tweets.zip'):
    r"""Extract the cached tweets "database" if necessary and load + parse the json.

    >>> js = load_tweets()
    >>> len(js)
    8000
    >>> js[0].keys()
    [u'contributors',
     u'truncated',
     u'text',
     u'is_quote_status',
     u'in_reply_to_status_id',
     u'id',
     u'favorite_count',
     u'source',
     u'retweeted',
     u'coordinates',
     u'entities',
     u'in_reply_to_screen_name',
     u'id_str',
     u'retweet_count',
     u'in_reply_to_user_id',
     u'favorited',
     u'user',
     u'geo',
     u'in_reply_to_user_id_str',
     u'possibly_sensitive',
     u'lang',
     u'created_at',
     u'in_reply_to_status_id_str',
     u'place',
     u'metadata']
    >>> print(json.dumps((obj for obj in js if obj['geo'] is not None).next(), indent=4))
    {
        "contributors": null,
        "truncated": false,
        "text": "See our latest #Sacramento, CA #job and click to apply: Python Software Engineer - https://t.co/yimTIlISE0 #IT #Hiring #CareerArc",
        "is_quote_status": false,
        "in_reply_to_status_id": null,
        "id": 674998672136929280,
        "favorite_count": 0,
        "source": "<a href=\"http://www.tweetmyjobs.com\" rel=\"nofollow\">TweetMyJOBS</a>",
        "retweeted": false,
        "coordinates": {
            "type": "Point",
            "coordinates": [
                -121.4399041,
                38.5963157
            ]
        },
        "entities": {
            "symbols": [],
            "user_mentions": [],
            "hashtags": [
                {
                    "indices": [
                        15,
                        26
                    ],
                    "text": "Sacramento"
                },
                {
                    "indices": [
                        31,
                        35
                    ],
                    "text": "job"
                },
                {
                    "indices": [
                        107,
                        110
                    ],
                    "text": "IT"
                },
                {
                    "indices": [
                        111,
                        118
                    ],
                    "text": "Hiring"
                },
                {
                    "indices": [
                        119,
                        129
                    ],
                    "text": "CareerArc"
                }
            ],
            "urls": [
                {
                    "url": "https://t.co/yimTIlISE0",
                    "indices": [
                        83,
                        106
                    ],
                    "expanded_url": "http://bit.ly/1OTNflo",
                    "display_url": "bit.ly/1OTNflo"
                }
            ]
        },
        "in_reply_to_screen_name": null,
        "id_str": "674998672136929280",
        "retweet_count": 0,
        "in_reply_to_user_id": null,
        "favorited": false,
        "user": {
            "follow_request_sent": null,
            "has_extended_profile": false,
            "profile_use_background_image": true,
            "id": 22634351,
            "verified": false,
            "profile_text_color": "000000",
            "profile_image_url_https": "https://pbs.twimg.com/profile_images/670049883869458435/J_Klv-BV_normal.jpg",
            "profile_sidebar_fill_color": "407DB0",
            "is_translator": false,
            "geo_enabled": true,
            "entities": {
                "url": {
                    "urls": [
                        {
                            "url": "https://t.co/DByWt45HZj",
                            "indices": [
                                0,
                                23
                            ],
                            "expanded_url": "http://www.careerarc.com/job-seeker",
                            "display_url": "careerarc.com/job-seeker"
                        }
                    ]
                },
                "description": {
                    "urls": []
                }
            },
            "followers_count": 452,
            "protected": false,
            "location": "Sacramento, CA",
            "default_profile_image": false,
            "id_str": "22634351",
            "lang": "en",
            "utc_offset": -18000,
            "statuses_count": 157,
            "description": "Follow this account for geo-targeted Software Dev.
                - General/IT job tweets in Sacramento, CA. Need help? Tweet us at @CareerArc!",
            "friends_count": 326,
            "profile_link_color": "4A913C",
            "profile_image_url": "http://pbs.twimg.com/profile_images/670049883869458435/J_Klv-BV_normal.jpg",
            "notifications": null,
            "profile_background_image_url_https": "https://pbs.twimg.com/profile_background_images/315958568/Twitter-BG_2_bg-image.jpg",
            "profile_background_color": "253956",
            "profile_banner_url": "https://pbs.twimg.com/profile_banners/22634351/1448587317",
            "profile_background_image_url": "http://pbs.twimg.com/profile_background_images/315958568/Twitter-BG_2_bg-image.jpg",
            "name": "TMJ-SAC IT Jobs",
            "is_translation_enabled": false,
            "profile_background_tile": false,
            "favourites_count": 0,
            "screen_name": "tmj_sac_it",
            "url": "https://t.co/DByWt45HZj",
            "created_at": "Tue Mar 03 15:28:22 +0000 2009",
            "contributors_enabled": false,
            "time_zone": "Eastern Time (US & Canada)",
            "profile_sidebar_border_color": "000000",
            "default_profile": false,
            "following": null,
            "listed_count": 36
        },
        "geo": {
            "type": "Point",
            "coordinates": [
                38.5963157,
                -121.4399041
            ]
        },
        "in_reply_to_user_id_str": null,
        "possibly_sensitive": false,
        "lang": "en",
        "created_at": "Thu Dec 10 17:06:38 +0000 2015",
        "in_reply_to_status_id_str": null,
        "place": {
            "country_code": "US",
            "url": "https://api.twitter.com/1.1/geo/id/b71fac2ee9792cbe.json",
            "country": "United States",
            "place_type": "city",
            "bounding_box": {
                "type": "Polygon",
                "coordinates": [
                    [
                        [
                            -121.576613,
                            38.43792
                        ],
                        [
                            -121.362715,
                            38.43792
                        ],
                        [
                            -121.362715,
                            38.685512
                        ],
                        [
                            -121.576613,
                            38.685512
                        ]
                    ]
                ]
            },
            "contained_within": [],
            "full_name": "Sacramento, CA",
            "attributes": {},
            "id": "b71fac2ee9792cbe",
            "name": "Sacramento"
        },
        "metadata": {
            "iso_language_code": "en",
            "result_type": "recent"
        }
    }
    """
    basename, ext = os.path.splitext(filename)
    json_file = basename + '.json'
    json_path = os.path.join(DATA_PATH, json_file)
    zip_path = os.path.join(DATA_PATH, basename + '.zip')
    if not os.path.isfile(json_path):
        zf = ZipFile(zip_path, 'r')
        zf.extract(json_file, DATA_PATH)
    with open(json_path, 'rUb') as f:
        return json.load(f)


def features(filename='tweets.zip'):
    """NotImplemented"""
    raise NotImplemented("Need to implement feature extraction.")
    js = load_tweets(filename)
    index = []
    table = []
    columns = [u'text', u'is_quote_status',
               u'in_reply_to_status_id', u'in_reply_to_user_id',
               u'favorited', u'favorite_count',  u'retweeted', u'retweet_count',
               u'source', u'coordinates',
               (u'user', u'id'), (u'user', u'followers_count'), (u'user', u'location'),
               (u'metadata', u'iso_language_code'),
               u'user',
               u'geo',
               u'in_reply_to_user_id_str',
               u'possibly_sensitive',
               u'lang',
               u'created_at',
               u'in_reply_to_status_id_str',
               u'place',
               ]

    for tweet in js:
        index += [int(tweet['id'])]
        txt += [tweet['text']]


