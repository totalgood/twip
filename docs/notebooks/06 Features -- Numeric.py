
# coding: utf-8

# In[3]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os

import pandas as pd
from matplotlib import pyplot as plt

from twip.constant import DATA_PATH


# In[4]:

import matplotlib
from IPython.display import display, HTML 
get_ipython().magic(u'matplotlib inline')
np = pd.np
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 250)
get_ipython().magic(u'pprint')


# In[5]:

df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), low_memory=False)
rawlen = len(df)
df.drop_duplicates('id_str', keep='last', inplace=True)
rawlen - len(df)


# In[5]:

# df.get_
df.get_dtype_counts()


# In[9]:

dtypes = pd.Series([df[v].dtype for v in df.columns], index=df.columns)
dtypes


# In[6]:

mask = [col for col in df.columns if df[col].dtype in (bool, float, np.dtype('int64'))]  # don't forget bool and int64 (not int)!
mask
numbers = df[mask]
numbers


# In[8]:

import gzip
with gzip.open(os.path.join(DATA_PATH, 'numbers.csv.gz'), 'wb') as f:
    numbers.to_csv(os.path.join(DATA_PATH, 'numbers.csv.gz'), encoding='utf-8')


# In[6]:

numbers = pd.read_csv(os.path.join(DATA_PATH, 'numbers.csv.gz'), compression='gzip', engine='python')


# In[7]:

[col for col in numbers.columns if 'follow' in col]


# In[11]:

numbers.columns = [col.replace(' ', '_') for col in numbers.columns]


# In[12]:

cols = [col for col in numbers.columns if 'follow' in col]


# In[19]:

numbers.user_followers_count.hist()
plt.yscale('log', noposy='clip')
plt.ylabel('Tweets')
plt.xlabel('Followers')


# In[20]:

# group by user ID before doing plots based on user stats like followers


# In[ ]:



