
# coding: utf-8

# In[1]:

from __future__ import division, print_function, absolute_import
from past.builtins import basestring

import os
import gzip

import pandas as pd

from twip.constant import DATA_PATH

from gensim.models import TfidfModel
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


# So the new things are LsiModel and scatmat

# In[3]:

from gensim.models import LsiModel
from twip.plot import scatmat


# Load cleaned tweet data  
# Don't forget to fix up the tokens!  
# Can you think of a better way to save a list of lists of strings?
# What about the raw, unprocessed unicode tweet text itself?

# In[6]:

import gzip
with gzip.open(os.path.join(DATA_PATH, 'datetimes.csv.gz'), 'rb') as f:
    nums = pd.read_csv(f, engine='python', encoding='utf-8')
with gzip.open(os.path.join(DATA_PATH, 'text.csv.gz'), 'rb') as f:
    corpus = pd.DataFrame.from_csv(f, encoding='utf8')


# Now load previously compiled vocabulary and TFIDF matrix (transformation)

# In[11]:

tfidf = TfidfModel.load(os.path.join(DATA_PATH, 'tfidf'))
tfidf.num_docs


# In[17]:

bows = pd.Series(vocab.doc2bow(toks) for toks in corpus.tokens)
bows


# This would make a nice, compact sparse matrix representation of our entire corpus...  
# Which would mean we could do more in RAM at once.  
# Left as an exercise.  (check out `scipy.sparse.coo_matrix`)  

# In[18]:

tfidf[bows[0]]


# In[19]:

dict([(vocab[i], freq) for i, freq in tfidf[bows[0]]])


# Notice how "you" didn't get as much weight as "enjoy"  
# Let's look at some other tweets  

# In[9]:

from gensim.models import LsiModel
lsi = LsiModel.load('../../data/lsi100')
len(lsi.id2word)


# This is starting to look a lot like a set of vectors that we could use as features  
# But wait, if I used the IDs as the vector index (column) numbers, how many features or "columns" would I have?

# In[ ]:

len(vocab)


# 100k dimensions isn't a good idea  
# Even for a masively parallel deep learning project this would be big  
# Like the cat/dog picture classification on 256x256 images  
# What about PCA (Principal Component Analysis) like is used on images?  
# In NLP PCA is called LSI (Latent Semantic Analysis)  
# That sounds cool!  
# I want me some latent semantics (hidden meaning)  

# In[ ]:

lsi = LsiModel(bows, num_topics=100, id2word=vocab, extra_samples=100, power_iters=2)
lsi


# ## That's Fast!  
# What happened to the **GIL**?  
# The gilectomy talk isn't until tomorrow!  
# Can Python do that?  
# With `numpy` and `gensim` it can.  

# What's that sound I hear?  
# That's the sound mof your fans blowing *hot air* out of those tweets!  
# (check out your system monitor or `htop`)  

# In[28]:

tweetids = pd.Series(range(6), name='tweet')
topicids = pd.Series(range(lsi.num_topics), name='topic')
pd.DataFrame([pd.Series([x[1] for x in lsi[bows[i]]], index=topicids,
                        name='tweet') for i in tweetids],
             index=tweetids)


# In[29]:

lsi2 = LsiModel(bows, num_topics=2, id2word=vocab, extra_samples=100, power_iters=2)
lsi2


# In[30]:

lsi.save(os.path.join(DATA_PATH, 'lsi100'))
lsi2.save(os.path.join(DATA_PATH, 'lsi2'))


# In[16]:

lsi2.show_topics()


# In[23]:

# for topic in lsi.show_topics():
#     print(topic)

lsi.show_topic(0, 100)


# ## Hold onto your hat
# This will take a lot of RAM!  
# (and CPU)  

# In[31]:

tweetids = pd.Series(range(len(bows)), name='tweet')
topicids = pd.Series(range(lsi.num_topics), name='topic')
# `dict()` keeps track of the columns for each topic, in case the lsi model shuffles or skips topics for odd tweets
df = pd.DataFrame([pd.Series(dict(lsi[bows[i]]), name='tweet') for i in tweetids],
                  columns=topicids,
                  index=tweetids)


# In[32]:

df


# What's with the 1.43?  
# Aren't they normalize?  
# ... Nope  

# In[12]:

scatmat(df[df.columns[:5]][::100])


# In[ ]:

num


# In[ ]:

with gzip.open(os.path.join(DATA_PATH, 'tweet_topic_vectors.csv.gz'), 'wb') as f:
    df.to_csv(f, encoding='utf8', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)


# We built LSI topic vectors for 200k tweets in a few minutes!  
# Lets look at the TFIDF vectors for the top 6 tweets

# In[10]:

tfidf6 = pd.DataFrame((dict([(vocab[i], freq) for i, freq in tfidf[bows[j]]]) for j in range(6)))
tfidf6 = tfidf6.fillna('')
tfidf6


# Notice the small weights on the word "Python"?
# Why do you think that is?
# (Think back to the definition of TF and DF and TFIDF

# Now lets see how far apart they are based only on word frequency (TFIDF)
# We'll *"project"* the first tweet onto the second with a dot product  
# to see how much of a "shadow" they make on each other  

# In[ ]:

tfidf6 = pd.DataFrame((dict([(vocab[i], freq) for i, freq in tfidf[bows[j]]]) for j in range(6))).fillna(0).T


# In[ ]:

np.dot(tfidf6[0], tfidf6[1])


# In[ ]:

np.dot(tfidf6[1], tfidf6[2])


# That looks about right.  
# The first 2 share no words.  
# The second 2 share only "Python".  
# But lets do the cosine similarity correctly by normalizing for length.  

# In[ ]:

np.dot(tfidf6[1], tfidf6[2]) / np.linalg.norm(tfidf6[1]) / np.linalg.norm(tfidf6[2])


# Hmmm, nothing changed  
# Can you guess why?  

# In[ ]:

[round(np.dot(tfidf6[i], tfidf6[i+1]), 4) for i in range(5)]


# In[ ]:

Now lets look at the topic vectors.  


# In[125]:

df.iloc[:6]


# In[122]:

print([round(np.dot(df.T[i], df.T[i+1]), 4) for i in range(5)])


# Better normalize these...

# In[123]:

print([round(np.dot(df.T[i], df.T[i+1]) / np.linalg.norm(df.T[i]) / np.linalg.norm(df.T[i+1]), 4) for i in range(5)])
# for comparison the TFIDF scores right below
print([round(np.dot(tfidf6[i], tfidf6[i+1]), 4) for i in range(5)])


# So the really chummy neighbors are 1 & 2 and 3 & 4  
# Surprisingly 2 & 3 didn't hit it off, and no pairing got a zero!   
# And the last 2 seem to share a "latent" similarity that TFIDF missed entirely!!!
# And LSI picked up on the python<->Python similarity (tweets 0 and 1)

# In[133]:

with gzip.open(os.path.join(DATA_PATH, 'text.csv.gz'), 'rb') as f:
    text = pd.DataFrame.from_csv(f, encoding='utf8')


# In[188]:

for toks, twt in zip(text.txt.iloc[:6], text.text.iloc[:6]):
    print(toks)
    print(twt)
    print('-' * 10)
    


# What about a new tweet you are considering?  
# Notice how I changed the token spelling (BOW),  
# but not the *"semantics"* of the tweet.  

# In[169]:

tweet = 'I want to help build django with a job in Chicago'
tweet_bow = vocab.doc2bow(tweet.split())
tweet_tfidf = tfidf[tweet_bow]
tweet_topics = pd.Series(dict(lsi[tweet_tfidf]))
# Now that the math is done let's convert to a friendlier format with words as the keys/index
tweet_tfidf = pd.Series(dict([(vocab[i], x) for (i, x) in tweet_tfidf])) 
print('\nLSI Topic Vector')
tweet_topics


# Compare the topic vector above to the TFIDF vector below.  
# What's better about TFIDF compared to topic vectors?  
# What can we do about it?  

# In[170]:

print('TFIDF Frequency Vector')
print(tweet_tfidf)


# Which one is it closest too?  
# Can you guess?  
# Does LSI understand the words as well as you do?  

# In[167]:

print('LSI Topic Similarity')
print([round(np.dot(df.T[i], tweet_topics) / np.linalg.norm(df.T[i]) / np.linalg.norm(tweet_topics), 4) for i in range(6)])


# In[184]:

tfidf7 = tfidf6.copy()
tfidf7[6] = tweet_tfidf
tfidf7 = tfidf7.fillna(0)
tfidf7


# In[ ]:




# In[186]:

print([round(np.dot(tfidf7[i], tfidf7[6]), 4) for i in range(6)])


# In[187]:

tweet


# Can you find the one word I accidentally share with the other tweets?  
# *Hint: use the TFIDF matrix (Dataframe)*  
# Play around with the tweet text to make its topic vector more *"orthogonal"*  
# Or make it closer in cosine distance.  
