#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Find json files (recursively) within the curent path
Load those that look like tweets dumped by tweetget
Expand columns that contain arrays, e.g. geo.coordinates -> geo.coordinates.lat and .lon
Combine each DataFrame into a single Pandas DataFrame
"""
from __future__ import division, print_function, absolute_import

import re
import json
import logging
import time

import pandas as pd
from matplotlib import pyplot as plt
import progressbar

from pug.nlp.util import find_files

np = pd.np
verbosity = 1

LOG_FORMAT = '%(levelname)-5s %(module)s.%(funcName)s:%(lineno)d %(message)s'
logging.basicConfig(format=LOG_FORMAT)
log = logging.getLogger(__file__)
if verbosity:
    log.setLevel(logging.DEBUG)

log.info('Finding json files...')
meta_files = find_files(ext='.json')
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
    df.set_index('id', inplace=True)
    if 'geo.coordinates' in df.columns:
        latlon = np.array([(ll[0], ll[1]) if isinstance(ll, list) else (np.nan, np.nan) for ll in df['geo.coordinates']])
        df['lat'] = zip(*latlon)[0]
        df['lon'] = zip(*latlon)[1]
    else:
        df['lat'] = np.nan * np.ones(len(df))
        df['lon'] = np.nan * np.ones(len(df)) 
    df_all = df_all.append(df)
    del df
    loaded_size += meta['size']
    if pbar:
        pbar.update(loaded_size / 1e6)
if pbar:
    pbar.finish()
log.info('Loaded {} unique tweets.'.format(len(df_all)))

filename = 'all_tweets.csv'
df_size = len(df_all) * 2402.9691 / 1e6

T0 = time.time()
log.info('Saving tweets in {} which should take around {:.1f} MB and {:.1f} min (utf-8 encoding in Pandas .to_csv is VERY slow)...'.format(
  filename, df_size, 0.6870573 * df_size / 60.))
df_all.to_csv(filename, encoding='utf-8')
T1 = time.time()
log.info('Saved {} tweets in {:.1f} min'.format(len(df_all), (T1 - T0) / 60.))
