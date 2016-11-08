from __future__ import unicode_literals

import pandas as pd


def try_int(s):
    try:
        return int(s)
    except:
        return None


def try_encode(s):
    try:
        return s.encode('utf-8')
    except:
        return None


def try_decode(s):
    try:
        return s.decode('utf-8')
    except:
        return s or None


def null2none(obj):
    if pd.isnull(obj):
        return None
    else:
        return obj


def clean_tweets(df, columns=None, text_columns=None):
    columns = columns or [c for c in df.columns if 'count' in c.lower() and 'country' not in c.lower()]
    for c in columns:
        df[c] = df[c].apply(try_int)
        print(c + ': ' + str(df[c].isnull().sum()))
    df = df[~df['user.favourites_count'].isnull()]
    df = df[~df['user.statuses_count'].isnull()]
    text_columns = text_columns or [c for c in df.columns if c.lower().endswith('text')]
    for c in text_columns:
        df[c] = df[c].apply(try_encode)
        print(c + ': ' + str(df[c].isnull().sum()))
