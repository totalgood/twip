
# coding: utf-8

# In[3]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os

import pandas as pd

from twip.constant import DATA_PATH
import string


# In[4]:

import matplotlib
from IPython.display import display, HTML 
get_ipython().magic(u'matplotlib inline')
np = pd.np
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)


# In[5]:

import gzip
from gensim.models import TfidfModel
from gensim.corpora import Dictionary


# Load previously cleaned data

# In[6]:

dates = pd.read_csv(os.path.join(DATA_PATH, 'datetimes.csv.gz'), engine='python')
nums = pd.read_csv(os.path.join(DATA_PATH, 'numbers.csv.gz'), engine='python')
with gzip.open(os.path.join(DATA_PATH, 'text.csv.gz'), 'rb') as f:
    df = pd.DataFrame.from_csv(f, encoding='utf8')
df.tokens


# In[7]:

d = Dictionary.from_documents(df.tokens)


# In[11]:

df.tokens.iloc[0]


# When we said "QUOTE_NONNUMERIC" we didn't mean **ALL** nonnumeric fields ;)

# In[16]:

df['tokens'] = df.txt.str.split()
df.tokens


# In[18]:

df.tokens.values[0:3]


# In[22]:

d = Dictionary.from_documents(df.tokens)
d


# In[20]:

tfidf = TfidfModel(d)


# *Hint-Hint:* `gensim` is sprinting this week at PyCon!

# In[24]:

get_ipython().magic(u'pinfo TfidfModel')


# In[26]:

TfidfModel(df.txt)


# In[27]:

TfidfModel(df.tokens)


# In[28]:

TfidfModel((d.doc2bow(tokens) for tokens in df.tokens))


# But there's a simpler way.  
# We already have a vocabulary  
# with term and document frequencies in a matrix...  

# In[33]:

pd.Series(d.dfs)


# In[34]:

pd.Series(d.iteritems())


# OK, now I get it  
# 
# - `document` is a list of strings (ordered sequence of tokens)  
# - `bow` or [bag of words] is a list of `Counter`-like mappings between word IDs and their count in each document
# - `TfidfModel` is a transformation from a BOW into a BORF,  a "bag of relative frequencies"  
# 
# TFIDF = BORF = term frequencies normalized by document occurence counts
# 

# In[37]:

pd.Series(d.doc2bow(toks) for toks in df.tokens[:3])


# Did it assign 0 to the first word it found?  
# Sort-of...  

# In[39]:

d.token2id['python']


# In[40]:

d.token2id['Python']


# In[41]:

d.token2id['you']


# In[8]:

d.id2token[0]  # guesses anyone?


# In[35]:

tfidf = TfidfModel(dictionary=d)
tfidf


# In[ ]:

tfidf.


# In[42]:

tfidf.num_docs


# In[43]:

tfidf.num_nnz


# In[44]:

tfidf.save(os.path.join(DATA_PATH, 'tfidf'))


# In[45]:

tfidf2 = TfidfModel.load(os.path.join(DATA_PATH, 'tfidf'))


# In[46]:

tfidf2.num_nnz

