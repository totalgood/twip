
# coding: utf-8

# In[1]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os

import pandas as pd

from twip.constant import DATA_PATH
import string


# In[2]:

import matplotlib
from IPython.display import display, HTML 
get_ipython().magic(u'matplotlib inline')
np = pd.np
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)


# In[3]:

df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), low_memory=False)


# In[4]:

df = df.drop_duplicates('id', keep='last')[['id', 'id_str', 'text']]
df.id == df.id_str
(df.id != df.id_str).sum()


# In[5]:

df = df[['id', 'text']]


# In[6]:

df.text


# In[8]:

df['tokens'] = df.text.str.split()
df


# In[9]:

from pug.nlp.regex import url
df['tokens'] = df.text.str.replace(url, '').str.split()
df


# In[10]:

df['txt'] = df.text.str.replace(url, ' ').str.replace(r'\W+', ' ').str.replace(r'\s+', ' ')
df.txt


# In[18]:

df['txt'] = df.txt.str.replace(r'\d+', ' ').str.replace(r'\s+', ' ')
df['tokens'] = df.txt.str.split()
df


# Notice that we trounced the hashtag #Python  
# That's not good.  
# Can you fix it?  
# Anything else we might be messing up?  
# *what other punctuation marks have special meaning in Tweets*  

# In[ ]:

# improve on the "stopword" filters here
#
# :-) (ask me about a smilie lexicon)
# not-so-simple words? (ask me about a regex for compound words)
# python variables names with underscores? (regex)


# In[7]:

f = os.path.join(DATA_PATH, 'text.csv.gz')
df.to_csv(f, encoding='utf8', compression='gzip', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)


# In[9]:

import gzip
with gzip.open(os.path.join(DATA_PATH, 'text.csv.gz'), 'wb') as f:
    df.to_csv(f, encoding='utf8', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)


# Make sure you can read it back in!

# In[10]:

df = pd.DataFrame.from_csv(os.path.join(DATA_PATH, 'text.csv.gz'))
df


# In[ ]:



