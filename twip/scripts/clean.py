#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Load, clean, and do some basic data exploration on the data

- load tweets (previously concatenated with cat_tweets) into a single DataFrame
- drop columns with mostly null values
- drop rows with mostly null values
- use DataFrame.describe to get basic stats on each column
- use pandas_profiler.ProfileReport to produce histograms, etc in HTML
"""
from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os
from decimal import Decimal
from traceback import print_exc

import progressbar
import pandas as pd

# you really want to be efficient about RAM, so user iter and itertools
# from itertools import izip
from twip.constant import DATA_PATH
from pug.nlp.util import make_name

np = pd.np


def clean_labels(df):
    # in iPython Notebook print out df.columns to show that many of them contain dots
    # rename the columns to be attribute-name friendly
    df.columns = [label.replace('.', '_') for label in df.columns]
    df.columns = [make_name(label) for label in df.columns]
    return df


def dropna(df, nonnull_rows=100, nonnull_cols=50, nanstr='nan', nanval=np.nan):
    if 0 < nonnull_rows < 1:
        nonnull_rows = int(nonnull_rows * len(df))
    if 0 < nonnull_cols < 1:
        nonnull_cols = int(nonnull_cols * len(df.columns))
    for label in df.columns:
        series = df[label].copy()
        strmask = np.array([isinstance(v, basestring) for v in series])
        notnanmask = strmask
        if not sum(notnanmask):
            continue
        print('Checking for {} nanstrings in {} column'.format(repr(nanstr), label))
        try:
            notnanmask[strmask] = notnanmask[strmask] & np.array(series[strmask] != nanstr)
        except TypeError:
            print("Unable to compare {} == {}".format(series[strmask], nanstr))
        notnanmask = notnanmask | ~strmask                  
        series[~notnanmask] = nanval
        df[label] = series
    # in iPython Notebook, try dropping with lower thresholds, checking column and row count each time
    print('The raw table shape is {}'.format(df.shape))
    df = df.dropna(axis=1, thresh=nonnull_rows)
    print('After dropping columns with fewer than {} nonnull values, the table shape is {}'.format(nonnull_rows, df.shape))
    df = df.dropna(axis=0, thresh=nonnull_cols)
    print('After dropping rows with fewer than {} nonnull values, the table shape is {}'.format(nonnull_cols, df.shape))
    return df


def normalize(df):
    """Flatten compound columns (DataFrames within columns) into top level columns"""
    # in ipython notebook, explore and describe the DataFrame columns
    print('Of the {} columns, {} are actually DataFrames'.format(len(df.columns), sum([not isinstance(df[col], pd.Series) for col in df.columns])))
    # remove dataframes with only 2 columns and one is the _str of the other:
    for col in df.columns:
        if isinstance(df[col], pd.DataFrame):
            print('Column {} is a {}-wide DataFrame'.format(col, len(df[col].columns)))
            if df[col].columns[1] == df[col].columns[0] + '_str':
                print('Column {} looks easy because it has sub-columns {}'.format(col, df[col].columns))
                df[col] = df[col][df[col].columns[1]]
            else:
                try:
                    assert(float(df[col].iloc[:, 0].max()) == float(df[col].iloc[:, 1].max()))
                    df[col] = df[col].fillna(-1, inplace=False)
                    series = pd.Series([int(Decimal(x)) for x in df[col].iloc[:, 1].values]).astype('int64').copy()
                    del df[col]
                    df[col] = series
                    print('Finished converting column {} to type {}({})'.format(col, type(df[col]), df[col].dtype))
                except:
                    print_exc()

    print('Of the {} columns, {} are still DataFrames after trying to convert both columns to long integers'.format(
        len(df.columns), sum([not isinstance(df[col], pd.Series) for col in df.columns])))
    return df


def encode(df, encoding='utf8', verbosity=1):
    """If you try to encode each element individually with python, this would take days!"""
    if verbosity > 0:
        # pbar_i = 0
        pbar = progressbar.ProgressBar(maxval=df.shape[1])
        pbar.start()
    # encode strings as UTF-8 so they'll work in python2 and python3
    for colnum, col in enumerate(df.columns):
        if isinstance(df[col], pd.Series):
            if verbosity:
                pbar.update(colnum)
            if df[col].dtype in (np.dtype('object'), np.dtype('U'), np.dtype('S')) and any(isinstance(obj, basestring) for obj in df[col]):
                strmask = np.array([isinstance(obj, basestring) for obj in df[col]])
                series = df[col].copy()
                try:
                    series[strmask] = np.char.encode(series[strmask].values.astype('U'))
                except TypeError:
                    print("Unable to convert {} elements starting at position {} in column {}".format(
                          sum(strmask), [i for i, b in enumerate(strmask) if b][:1], col))
                    raise
                except UnicodeDecodeError:
                    try:
                        series[strmask] = np.array([eval(s, {}, {}) for s in series[strmask]])
                    except (SyntaxError, UnicodeDecodeError):
                        newseries = []
                        for s in series[strmask]:
                            try:
                                newseries += [s.encode('utf8')]
                            except:
                                print(u'Had trouble encoding {} so used repr to turn it into {}'.format(s, repr(s)))
                                newseries += [repr(s)]
                        series[strmask] = np.array(newseries).astype('U')
                df[col] = series
                # df[col] = np.array([x.encode('utf8') if isinstance(x, unicode) else x for x in df[col]])

            # WARNING: this takes DAYS for only 100k tweets!
            # series = df[col].copy()
            # for i, value in series.iteritems():   

            #     if isinstance(value, basestring):
            #         series[i] = str(value.encode(encoding))
            # df[col] = series
    if verbosity:
        pbar.finish()
    return df

def run():
    """Load all_tweets.csv and run normalize, dropna, encode before dumping to cleaned_tweets.csv.gz

    Many columns have "mixed type" to `read_csv` should set `low_memory` to False to ensure they're loaded accurately
    >>> df2 = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), index_col='id', compression='gzip', quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
    /home/hobs/.virtualenvs/twip/local/lib/python2.7/site-packages/IPython/core/interactiveshell.py:2723:
    DtypeWarning: Columns (74,82,84,105,114,115,116,117,118,119,120,121,122,123,125,126,127,128,129,130,132,133,134,135,136,137,138,139,140,141,142,143,144,145,146,147,149,150,151,152,199,200,202,203,210,211,214,215,223,231,232,238) have mixed types. Specify dtype option on import or set low_memory=False.
       interactivity=interactivity, compiler=compiler, result=result)
    """
    verbosity = 1
    filepath = os.path.join(DATA_PATH, 'all_tweets.csv')
    # this should load 100k tweets in about a minute
    # check the file size and estimate load time from that (see json_to_dataframe.py)
    print('Loading tweets (could take a minute or so)...')
    df = pd.read_csv(filepath, encoding='utf-8', engine='python')
    if 'id' in df.columns:
        df = df.set_index('id')
    df = normalize(df)
    df = dropna(df)
    df = encode(df, verbosity=verbosity)
    df.to_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), compression='gzip',
              quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    # the round-trip to disk cleans up encoding issues so encotding no longer needs to be specified on load
    df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), index_col='id', compression='gzip',
                     quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
    df.to_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), compression='gzip',
              quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    return df