
# coding: utf-8

# In[3]:

import os

import pandas as pd
import matplotlib
import seaborn

from twip.constant import DATA_PATH

get_ipython().magic(u'matplotlib inline')
from IPython.display import display, HTML 
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 12)


# In[4]:

tfdf = pd.read_csv(os.path.join(DATA_PATH, 'tweet_vocab.csv.gz'), index_col=0, compression='gzip',
                   quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
tfdf.describe()


# If you try to allocate a 16k word by 100k document DataFrame of 64-bit integers, you'll get a memory error on a 16 GB laptop.  
# Later we'll learn about "constant RAM" tools that can handle an unlimitted stream of documents with a large (1M word) vocabulary. But first let's be frugal and see what we can do with robust, mature tools like Pandas.  
# Rather than cutting back on those 100k tweets, lets cut back on the words. What are all those 16k words and how often are they all used (maybe we can ignore infrequent words).  

# In[16]:

GB = 8 * (100 * 1000 * len(tfdf)) / 1.e9
GB


# In[6]:

tfdf


# Fortunately the odd words are at the top and bottom of an alphabetical index!  
# And it does look like the less useful tokens aren't used many times or in many documents.  
# What do you notice that might help distinguish "natural" words (zoom, zoos, zope, zynga) from URLs and machine-code (000, zzp, zsl107)?  

# In[11]:

tfdf = tfdf[tfdf.df > 9]
tfdf = tfdf[(tfdf.df > 9) & (((tfdf.df - tfdf.tf) / tfdf.tf) < 0.15)]
tfdf = tfdf[(tfdf.df > 20) & (((tfdf.df - tfdf.tf) / tfdf.tf) < 0.15)]
tfdf


# In[ ]:

Numpy arrays (guts of Pandas DataFrame) require 8 bytes for each double-precision value (int64)


# In[14]:

GB = 8 * (100 * 1000 * len(tfdf)) / 1.e9
GB


# Memory requirements (4 GB) are doable  
# But we've lost important words: **"zoom"**  
# And there's still a bit of garbage: **"zh3gs0wbno"**  
# These look like keys, slugs, hashes or URLs  
# Even though the tweets.json format includes a column for URLs  
# The URLs are left within the raw text as well  
# Let's use a formal but simple grammar engine:
# 
# ## Extended regular expressions 

# In[27]:

from pug.nlp import constant
# constant.uri_schemes_popular = ['chrome', 'https', 'http', ]
url_scheme_popular = r'(\b(' + '|'.join(constant.uri_schemes_popular) + r')[:][/]{2})'
fqdn_popular = r'(\b[a-zA-Z0-9-.]+\b([.]' + r'|'.join(constant.tld_popular) + r'\b)\b)'
url_path = r'(\b[\w/?=+#-_&%~\'"\\.,]*\b)'

pd.set_option('display.max_rows', 14)
pd.Series(constant.uri_schemes_iana)


# In[28]:

url_popular = r'(\b' + r'(http|https|svn|git|apt)[:]//' + fqdn_popular + url_path + r'\b)'
tweet = "Play the [postiive sum game](http://totalgood.com/a/b?c=42) of life instead of svn://us.gov."
import re
re.findall(url_popular, tweet)


# In[ ]:



