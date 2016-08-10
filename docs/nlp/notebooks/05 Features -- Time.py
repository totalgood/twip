
# coding: utf-8

# In[1]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os
from collections import Counter

import pandas as pd
from matplotlib import pyplot as plt 

from twip.constant import DATA_PATH


# In[2]:

import matplotlib
from IPython.display import display, HTML 
get_ipython().magic(u'matplotlib inline')
np = pd.np
display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 8)
pd.set_option('display.max_columns', 250)
get_ipython().magic(u'pprint')


# In[6]:

import gzip
with gzip.open(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), 'rb') as f:
    df = pd.read_csv(f, encoding='utf8', low_memory=False)
rawlen = len(df)
df.drop_duplicates('id_str', keep='last', inplace=True)
rawlen - len(df)


# In[ ]:




# In[ ]:

mask = np.array([bool('date' in c) for c in df.columns])
df.columns[mask]


# In[ ]:

df.columns[np.array([bool('time' in c) for c in df.columns])]


# Remember any date or time columns from Dan's tutorial?

# In[8]:

mask = np.array([c.endswith('_at') for c in df.columns])
df.columns[mask]


# In[9]:

dates = df[df.columns[mask]]
dates


# In[10]:

dates = pd.DataFrame(index=df.index)
for col in df.columns[np.array([bool(c.endswith('_at')) for c in df.columns])]:
    print(col)
    dates[col] = pd.to_datetime(df[col])


# In[30]:

dates


# In[11]:

import gzip
with gzip.open(os.path.join(DATA_PATH, 'datetimes.csv.gz'), 'wb') as f:
    dates.to_csv(f, encoding='utf8')
    # dates.to_csv(os.path.join(DATA_PATH, 'datetimes.csv.gz'), compression='gzip')


# In[36]:

get_ipython().magic(u'ls -thal DATA_PATH')
get_ipython().system(u'ls -thal data')


# In[43]:

system("ls %s" % DATA_PATH)


# In[45]:

ls -thal ../../data


# In[12]:

dates = pd.read_csv(os.path.join(DATA_PATH, 'datetimes.csv.gz'), engine='python')

for col in dates.columns:
    print(col)
    dates[col] = pd.to_datetime(dates[col])


# In[13]:

dates.created_at.dt.hour


# In[8]:

dates.created_at.dt.weekday


# In[23]:

dow = pd.Series(dates.created_at.dt.weekday)
dow.hist(bins=[0,1,2,3,4,5,6,7])
plt.xlabel('0=Mon    6=Sun')
plt.ylabel('Tweets')


# In[18]:

nums = pd.read_csv(os.path.join(DATA_PATH, 'numbers.csv.gz'), engine='python')


# In[19]:

features = pd.DataFrame({'faves': nums.favorite_count, 'weekday': dow})


# In[24]:

names = pd.Series([''] * len(dow), index=dow.index)
for i, label in enumerate('Mon Tues Wed Thurs Fri Sat Sun'.split()):
    names[dow == i] = label


# In[33]:

faves_by_dow = pd.Series(Counter(names[nums.favorite_count > 0]))
faves_by_dow


# In[34]:

fave_ratio_by_dow = pd.Series(Counter(names[nums.favorite_count > 0])) / pd.Series(Counter(names))
fave_ratio_by_dow


# Keep in mind, these aren't big differences  
# And we have a sample bias ("Python" in May)

# Now it's your turn  
# Can you do a similar analysis for Time of Day  
# Hint: think of a good "bin" size  
# Use tab-completion on the `dt` accessor method of the dates you are interested in  
