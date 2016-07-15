#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Combine and normalize tweet.json files into a DataFrame dumped to csv

- Find json files (recursively) within the curent path
- Load those that look like tweets dumped by tweetget
- Expand columns that contain arrays, e.g. geo.coordinates -> geo.coordinates.lat and .lon
- Combine each DataFrame into a single Pandas DataFrame
- Save utf-8 encoded csv file of the normalized/combined DataFrame
"""
from __future__ import division, print_function, absolute_import

# pip install future
import builtins as base

import os
import re
import json
import logging
import time

import pandas as pd
import progressbar

from pug.nlp.util import find_files
from twip.constant import DATA_PATH

import argparse
import sys

from twip import __version__

__author__ = "hobs"
__copyright__ = "hobs"
__license__ = "mit"

np = pd.np
log = logging.getLogger(__name__)
LOG_FORMAT = '%(levelname)-5s %(module)s.%(funcName)s:%(lineno)d %(message)s'


def parse_args(args):
    """
    Parse command line parameters

    :param args: command line parameters as list of strings
    :return: command line parameters as :obj:`argparse.Namespace`
    """
    parser = argparse.ArgumentParser(
        description="Concatenate and preprocess tweet json files dumped by tweetget")
    parser.add_argument(
        '-v',
        '--verbose',
        help='Whether to show progress messages on stdout',
        action='store_true')
    parser.add_argument(
        '--version',
        help='print twip package version and exit.',
        action='version',
        version='twip {ver}'.format(ver=__version__))
    parser.add_argument(
        '-p',
        '--path',
        help='path to data dir (json input and csv output files)',
        default=DATA_PATH)
    parser.add_argument(
        '-t',
        '--tweetfile',
        help='file to store normalized table (csv) of tweets and features (metadata)',
        default='all_tweets.csv')
    parser.add_argument(
        '-n',
        '--numtweets',
        help='maximum number of tweets to process',
        type=int,
        default=1000000)
    parser.add_argument(
        '-g',
        '--geofile',
        help="file to store tweet lat/lon information (few use it)",
        default='geo_tweets.csv')
    return parser.parse_args(args)


def main(args):
    """API with args object containing configuration parameters"""
    global logging, log

    args = parse_args(args)
    logging.basicConfig(format=LOG_FORMAT,
                        level=logging.DEBUG if args.verbose else logging.INFO,
                        stream=sys.stdout)
    df = cat_tweets(path=args.path, verbosity=args.verbose + 1, numtweets=args.numtweets)
    log.info('Combined {} tweets'.format(len(df)))
    df = drop_nan_columns(df)
    save_tweets(df, path=args.path, filename=args.tweetfile)
    geo = get_geo(df, path=args.path, filename=args.geofile)
    log.info("Combined {} tweets into a single file {} and set asside {} geo tweets in {}".format(
        len(df), args.tweetfile, len(geo), args.geofile))
    return df, geo


def run():
    """Entry point for command line script"""
    main(sys.argv[1:])


def cat_tweets(filename='all_tweets.json', path=DATA_PATH, verbosity=1, numtweets=10000000, ignore_suspicious=True):
    """Find json files that were dumped by tweetget and combine them into a single CSV

    Normalize some (lat/lon)"""

    log.info('Finding json files...')
    meta_files = find_files(path=path, ext='.json')
    meta_files = [meta for meta in meta_files
                  if re.match(r'^201[5-6]-[0-9]{2}-[0-9]{2}\s[0-9]{2}[:][0-9]{2}[:][0-9]{2}[.][0-9]+[.]json$', meta['name'])]
    log.info('Found {} files that look like tweetget dumps.'.format(len(meta_files)))

    total_size = sum([meta['size'] for meta in meta_files])
    if verbosity > 0:
        pbar = progressbar.ProgressBar(maxval=(total_size + 1.) / 1e6)
        pbar.start()
    else:
        pbar = None

    loaded_size = 0
    df_all = pd.DataFrame()
    for meta in meta_files:
        df = pd.io.json.json_normalize(pd.json.load(open(meta['path'])))
        # json entries were dumped in reverse time order (most recent first)
        df.drop_duplicates(['id'], keep='first', inplace=True)
        df.set_index('id', drop=True, inplace=True)
        if 'geo.coordinates' in df.columns:
            latlon = np.array([(ll[0], ll[1]) if isinstance(ll, list) else (np.nan, np.nan) for ll in df['geo.coordinates']])
            for i, ll in enumerate(latlon):
                try:
                    latlon[i] = float(ll[0]), float(ll[1])
                except ValueError:
                    latlon[i] = np.nan, np.nan
            df['lat'] = zip(*latlon)[0]
            df['lon'] = zip(*latlon)[1]
            df_all = df_all.append(df)
        else:
            log.warn('Oddly the DataFrame in {} didnt have a geo.coordinates column.'.format(meta['path']))
            df['lat'] = np.nan * np.ones(len(df))
            df['lon'] = np.nan * np.ones(len(df))
            if not ignore_suspicious:
                log.warn('Skipping {} tweets!!!!.'.format(len(df)))
                df_all = df_all.append(df)
        # this would be a good time to incrementally save these rows to disc
        del df
        loaded_size += meta['size']
        if len(df_all) >= numtweets:
            # FIXME use average rate of 400 tweets/MB to calculate better progressbar size at start
            break
        if pbar:
            pbar.update(loaded_size / 1e6)
    if pbar:
        pbar.finish()
    log.info('Loaded {} unique tweets.'.format(len(df_all)))
    return df_all


def drop_nan_columns(df, thresh=325):
    """Drop columns that are mostly NaNs

    Excel files can only have 256 columns, so you may have to drop a lot in order to get down to this
    """
    if thresh < 1:
        thresh = int(thresh * df)
    return df.dropna(axis=1, thresh=thresh, inplace=False)


def drop_columns(df, columns=u'common_columns.json'):
    # df_all = drop_columns(df_all)
    # common_columns = json.dump(list(df_all.columns), open(os.path.join(DATA_PATH, 'common_columns.json'), 'w'), indent=0)
    if isinstance(columns, base.str):
        columns = json.load(open(os.path.join(DATA_PATH, columns), 'r'))
    df = df[columns].copy()
    df.dropna(how='all', inplace=True)


def get_geo(df, path=DATA_PATH, filename=u'geo_tweets.csv'):
    path = path.encode()
    try:
        geo = df[~df.lat.isnull() & ~df.lon.isnull()].copy()
    except AttributeError:
        geo = pd.DataFrame(columns=df.columns)
    if isinstance(filename, base.str):
        geo.to_csv(os.path.join(path, filename), encoding='utf8',
                   escapechar=None, quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    return geo


def save_tweets(df, path=DATA_PATH, filename=u'all_tweets.csv'):
    path = path.encode()
    filename = os.path.join(path, filename)
    # your first "model": predict the size of a file based on the number of rows of tweet data (average rate = linear regression)
    df_size = len(df) * 2403 / 1e6

    T0 = time.time()
    log.info('Saving {} tweets in {} which should take around {:.1f} MB and {:.1f} min (utf-8 encoding in Pandas .to_csv is VERY slow)...'.format(
             len(df), filename, df_size, 2.0 * df_size / 60.))
    # consider using to_csv(compression='gzip', escapechar=None) 
    try:
        df.to_csv(os.path.join(path, filename), encoding='utf8', compression='gzip', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    except ValueError:  # encoding + compression not yet supported in Python 2
        df.to_csv(os.path.join(path, filename), encoding='utf8', quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    T1 = time.time()
    log.info('Saved {} tweets in {:.1f} min'.format(len(df), (T1 - T0) / 60.))


if __name__ == "__main__":
    run()
