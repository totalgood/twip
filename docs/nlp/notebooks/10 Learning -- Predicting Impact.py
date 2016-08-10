
# coding: utf-8

# In[1]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os
import gzip

import pandas as pd

from twip.constant import DATA_PATH

from gensim.models import TfidfModel, LsiModel
from gensim.corpora import Dictionary


# In[2]:

import matplotlib
from IPython.display import display, HTML 
get_ipython().magic(u'matplotlib inline')
np = pd.np
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 6)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)
pd.set_option('precision', 2)
get_ipython().magic(u'precision 4')
get_ipython().magic(u'pprint')


# In[3]:

from sklearn.discriminant_analysis import LinearDiscriminantAnalysis


# In[4]:

lsi = LsiModel.load(os.path.join(DATA_PATH, 'lsi100'))
lsi2 = LsiModel.load(os.path.join(DATA_PATH, 'lsi2'))


# In[5]:

with gzip.open(os.path.join(DATA_PATH, 'tweet_topic_vectors.csv.gz'), 'rb') as f:
    topics = pd.DataFrame.from_csv(f, encoding='utf8')
topics = topics.fillna(0)


# In[6]:

topics


# In[7]:

dates = pd.read_csv(os.path.join(DATA_PATH, 'datetimes.csv.gz'), engine='python')
nums = pd.read_csv(os.path.join(DATA_PATH, 'numbers.csv.gz'), engine='python')


# When I first ran this, my dataframes weren't "aligned".  
# So it's very important to check your datasets after every load.  
# The correspondence between dates and topics and numerical features is critical for training!  

# In[155]:

print(len(dates))
print(len(topics))
print(len(nums))


# In[156]:

sum(nums.index == dates.index) == len(dates)


# In[157]:

sum(nums.index == topics.index) == len(dates)


# In[158]:

disc = LinearDiscriminantAnalysis()
disc


# In[159]:

features = pd.concat((topics, nums.favorite_count), axis=1)
features


# In[160]:

disc = LinearDiscriminantAnalysis().fit(topics, nums.favorite_count >= 1)


# In[161]:

predicted_favorites = disc.predict(topics)
predicted_favorites


# In[162]:

np.sum(predicted_favorites)


# ## Wow!  
# DiscriminantAnalysis is VERY discriminating!

# In[163]:

np.sum(nums.favorite_count >= 1)


# But not in a good way.  
# 10x more true favorites than predicted. 
# Our unbalanced training set makes it easy for the judge to be tough.  
# Let's mellow our judge a bit...  

# In[164]:

from pug.nlp.stats import Confusion


# In[165]:

results = pd.DataFrame()
results['predicted'] = predicted_favorites
results['truth'] = pd.Series(nums.favorite_count >= 1)
conf = Confusion(results)
conf


# In[166]:

results.predicted.corr(results.truth)


# In[167]:

conf.stats_dict


# High accuracy, but low MCC (correlation)

# Balance the training?  
# Get rid of some negatives?  
# **Accentuate the positive?** <-- give this a try yourself

# In[168]:

pos = np.array(nums.favorite_count >= 1)
neg = ~pos
portion_pos = float(sum(pos)) / len(nums)
mask = ((np.random.binomial(1, portion_pos, size=len(nums)).astype(bool) & neg) | pos)
disc = LinearDiscriminantAnalysis().fit(topics[mask], (nums.favorite_count[mask] >= 1))
print(sum(mask))
print(sum(pos) * 2)


# In[169]:

results = pd.DataFrame()
results['predicted'] = disc.predict(topics.values)
results['truth'] = nums.favorite_count.values >= 1
conf = Confusion(results)
conf


# In[170]:

results.predicted.corr(results.truth)


# In[171]:

conf.stats_dict


# So let's add some more negative examples back in.  
# 50x imbalance is defintiely misleading.  
# But 2-5x imbalance is probably OK.  

# In[172]:

portion_neg = 3 * portion_pos
mask = ((np.random.binomial(1, portion_neg, size=len(nums)).astype(bool) & neg) | pos)
disc = LinearDiscriminantAnalysis().fit(topics[mask], nums.favorite_count[mask] >=1 )
print(sum(mask))
print(sum(pos) * 2)


# In[173]:

results = pd.DataFrame()
results['predicted'] = disc.predict(topics.values)
results['truth'] = nums.favorite_count.values > 0
conf = Confusion(results)
conf


# At least the confusion matrix looks balanced now

# In[174]:

results.predicted.corr(results.truth)


# Should have known, imbalance doesn't help...

# In[179]:

portion_neg = 2 * portion_pos
mask = ((np.random.binomial(1, portion_neg, size=len(nums)).astype(bool) & neg) | pos)
disc = LinearDiscriminantAnalysis().fit(topics.values[mask], (nums.favorite_count.values > 0)[mask])
print(sum(mask))
print(sum(pos) * 2)


# In[180]:

results = pd.DataFrame()
results['predicted'] = disc.predict(topics.values)
results['truth'] = nums.favorite_count.values > 0
conf = Confusion(results)
conf


# In[181]:

results.predicted.corr(results.truth)


# So it looks like 38% correlation is all we can squeeze out of this simple model  
# Next up... adding number of followers and other features  
