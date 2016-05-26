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
# from past.builtins import basestring

import os

import pandas as pd
import pandas_profiling


# you really want to be efficient about RAM, so user iter and itertools
# from itertools import izip
from twip.constant import DATA_PATH

from pug.nlp.util import dict2obj

# the round-trip to disk cleans up encoding issues so encoding option no longer needs to be specified and gzip 
df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), index_col='id', compression='gzip',
                  quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)


print('df.describe() stats:')
desc = df.describe()
for col, stats in desc.T.iterrows():
    print('')
    print('{} ({})'.format(col, df[col].dtype if isinstance(df[col], pd.Series) else type(df[col])))
    print(stats)

html = pandas_profiling.to_html(df.head(3), desc)
open('report.html', 'w').write(html)

# this is redundant with stats above and takes way longer than it should (30 minutes?)
# print('Column, Count, Min, Mean, Max:')
# for k, c, colmin, colmean, colmax in izip(df.columns, df.count().T, df.min().T, df.mean().T, df.max().T):
#     print('{:40s}\t{}\t{}\t{}\t{}'.format(k, c, colmin, colmean, colmax))

# this takes a few minutes
print('Trying to compute a ProfileReport, including correlation between columns, skew etc')
# pandas_profiling.ProfileReport raises Tkinter exceptions before it can produce any output,
#  at least describe produces a dataframe of stats
report = dict2obj(pandas_profiling.describe(df))
print(report['table'])

print('')
for col, stats in report['variables'].iterrows():
    print('')
    print(col)
    # print('{} ({})'.format(col, df[col].dtype if isinstance(df[col], pd.Series) else type(df[col])))
    print(stats)

print('')
for col, stats in report['freq'].iteritems():
    print('')
    print(stats)

