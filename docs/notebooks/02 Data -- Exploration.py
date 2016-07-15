
# coding: utf-8

# In[1]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import matplotlib
get_ipython().magic(u'matplotlib inline')
from IPython.display import display, HTML 

import os
from decimal import Decimal
from traceback import print_exc

import pandas as pd
import pandas_profiling

# you really want to be efficient about RAM, so user iter and itertools
# from itertools import izip
from twip.constant import DATA_PATH
from pug.nlp.util import dict2obj

np = pd.np


# In[2]:

display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)


# In[3]:

print('Loading previously "cleaned" tweets (could take a minute or so)...')
df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), index_col='id', compression='gzip',
                 quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
print('Loaded {} tweets.'.format(len(df)))


# In[18]:

print('df.describe() stats:')
short_desc = df.describe()
for col, stats in short_desc.T.iterrows():
    print('{} ({})'.format(col, df[col].dtype if isinstance(df[col], pd.Series) else type(df[col])))
    print(dict(zip(list(stats.index.values[[0,1,2,3,7]].T), list(stats.values[[0,1,2,3,7]].T))))
    


# In[ ]:

# this takes a few minutes
print('Using pandas_profiling to generate more detailed stats, including correlation between columns, skew etc')
# pandas_profiling.ProfileReport raises Tkinter exceptions before it can produce any output,
#  at least describe produces a dataframe of stats
desc = pandas_profiling.describe(df)
desc['table']
# for col, stats in desc['variables'].iterrows():
#     print('')
#     print(col)
#     print('{} ({})'.format(col, df[col].dtype if isinstance(df[col], pd.Series) else type(df[col])))
#     print(stats)

# and if you thought that was tough to read, try printing out all the report['freq'] dicts of histograms


# In[43]:

desc['variables']


# In[38]:

desc['table']


# In[29]:

# desc.keys()
html = pandas_profiling.to_html(df.head(), desc).encode('utf8')
with open('report.html', 'w') as fout:
    fout.write(html)
display(HTML(html))
# report = pandas_profiling.ProfileReport(df)

