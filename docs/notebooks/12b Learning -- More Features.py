
# coding: utf-8

# In[2]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os
import gzip

import pandas as pd

from twip.constant import DATA_PATH

from gensim.models import TfidfModel, LsiModel


# In[7]:

lsi = LsiModel.load(os.path.join(DATA_PATH, 'lsi100'))
lsi2 = LsiModel.load(os.path.join(DATA_PATH, 'lsi2'))


# In[31]:

with gzip.open(os.path.join(DATA_PATH, 'tweet_topic_vectors.csv.gz'), 'rb') as f:
    topics = pd.DataFrame.from_csv(f, encoding='utf8')
topics = topics.fillna(0)


# In[5]:

dates = pd.read_csv(os.path.join(DATA_PATH, 'datetimes.csv.gz'), engine='python')
nums = pd.read_csv(os.path.join(DATA_PATH, 'numbers.csv.gz'), engine='python')


# In[7]:

weekday = dates.created_at.dt.weekday
hour = dates.created_at.dt.hour


# In[ ]:



