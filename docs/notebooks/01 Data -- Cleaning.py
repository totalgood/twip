
# coding: utf-8

# In[6]:

from __future__ import division, print_function, absolute_import

import os
from decimal import Decimal
from traceback import print_exc

import pandas as pd
import pandas_profiling

# you really want to be efficient about RAM, so user iter and itertools
# from itertools import izip
from twip.constant import DATA_PATH

import matplotlib
get_ipython().magic(u'matplotlib inline')


# In[7]:

# this should load 100k tweets in about a minute
print('Loading tweets (could take a minute or so)...')
df = pd.read_csv(os.path.join(DATA_PATH, 'all_tweets.csv'), index_col='id', engine='python', encoding='utf-8',
                 quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
# in iPython Notebook print out df.columns to show that many of them contain dots
# rename the columns to be attribute-name friendly
df.columns = [label.replace('.', '_') for label in df.columns]
print('Done.')


# In[8]:

print('The raw table shape is {}'.format(df.shape))
nonnull_rows = 330
nonnull_cols = 50
df = df.dropna(axis=1, thresh=nonnull_rows)
print('After dropping columns with fewer than {} nonnull values, the table shape is {}'.format(nonnull_rows, df.shape))
df = df.dropna(axis=0, thresh=nonnull_cols)
print('After dropping rows with fewer than {} nonnull values, the table shape is {}'.format(nonnull_cols, df.shape))


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


# In[9]:

print('df.describe() stats:')
desc = df.describe()
for col, stats in desc.T.iterrows():
    print('')
    print('{} ({})'.format(col, df[col].dtype if isinstance(df[col], pd.Series) else type(df[col])))
    print(stats)


# In[10]:

# this takes a few minutes
print('Using pandas_profiling to generate more detailed stats, including correlation between columns, skew etc')
# pandas_profiling.ProfileReport raises Tkinter exceptions before it can produce any output,
#  at least describe produces a dataframe of stats
report = pandas_profiling.describe(df)
print(report['table'])

print('')
for col, stats in report['variables'].iterrows():
    print('')
    print(col)
    # print('{} ({})'.format(col, df[col].dtype if isinstance(df[col], pd.Series) else type(df[col])))
    print(stats)

# and if you thought that was bad, try printing out all the report['freq'] dict of histograms

