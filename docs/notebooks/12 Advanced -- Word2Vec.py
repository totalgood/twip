
# coding: utf-8

# In[1]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os
import gzip

import pandas as pd

from twip.constant import DATA_PATH



# In[ ]:

import matplotlib
from IPython.display import display, HTML 
get_ipython().magic(u'matplotlib inline')
np = pd.np
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 800)
pd.set_option('precision', 2)
get_ipython().magic(u'precision 4')
get_ipython().magic(u'pprint')


# In[3]:

from gensim.models import Word2Vec


# For now let's use the Google News model (300 topics)

# In[4]:

wv = Word2Vec.load_word2vec_format(os.path.join(DATA_PATH, 'GoogleNews-vectors-negative300.bin.gz'), binary=True)


# In[7]:

wv.most_similar(positive=['python', 'snake',], negative=['programming'])


# In[9]:

wv.most_similar(positive=['PyCon'])


# In[15]:

wv.most_similar(positive=['Portland', 'Oregon', ], negative=['city', 'government'])

