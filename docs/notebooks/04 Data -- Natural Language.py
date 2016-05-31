
# coding: utf-8

# In[1]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import matplotlib
get_ipython().magic(u'matplotlib inline')
from IPython.display import display, HTML 
HTML("<style>.container { width:100% !important; }</style>")

import os
from decimal import Decimal
from traceback import print_exc

import pandas as pd

from twip.constant import DATA_PATH
from pug.nlp.util import dict2obj

np = pd.np


# In[ ]:




# Let's look at some tweets

# In[2]:

print('Loading previously "cleaned" tweets (could take a minute or so)...')
df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), index_col='id', compression='gzip',
                 quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
print('Loaded {} tweets.'.format(len(df)))
df


# In[3]:

text = df.text.iloc[:10]
for tweet in text:
    print()
    print(tweet)
    # print(repr(tweet))


# So Even after subtracting "-Monty" in our search query, there are still a lot more meanings for Python than we intended  
# This is one of the key challenges of natural language procesing, "ambiguity"  
# There are a lot of names for dimension reduction techniques that attempt to determing meaning (semantics) from bag of words statistics (words used near each other) 
#     
# - Word2Vec
# - LSI: Latent Semantic Indexing
# - PCA: Principal Component Analysis
# - SVD: Singular Value Decomposition
# 
# - LDA: Linear Discriminant Analysis
# - LDA: Latent Dirichlet Allocation
# 
