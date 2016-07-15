import os
import gzip

import pandas as pd

from gensim.models import TfidfModel
from gensim.corpora import Dictionary

from twip.constant import DATA_PATH


np = pd.np

dates = pd.read_csv(os.path.join(DATA_PATH, 'datetimes.csv.gz'), engine='python')
nums = pd.read_csv(os.path.join(DATA_PATH, 'numbers.csv.gz'), engine='python')
with gzip.open(os.path.join(DATA_PATH, 'text.csv.gz'), 'rb') as f:
    df = pd.DataFrame.from_csv(f, encoding='utf8')
d = Dictionary.from_documents(df.tokens)
# fail

df.tokens[0]
df.tokens
df.tokens.iloc[0]
df['tokens'] = df.txt.str.split()
df.tokens
df.tokens.iloc[0]
d = Dictionary.from_documents(df.txt.str.split())
len(d)
tfidf = TfidfModel(d)
tfidf = TfidfModel(dictionary=d)
tfidf
len(tfidf)
df.tokens[0]
df.tokens.iloc[0]
tfidf[df.tokens.iloc[0]]
d.doc2bow(df.tokens.iloc[0])
d.doc2bow(df.tokens.iloc[1])
d.doc2bow(df.tokens.iloc[2])
df.tokens.iloc[0:2]
df.tokens.iloc[0:3]
d['python']
d.token2id('python')
d.token2id['python']
d.token2id['you']
d.id2token[0]
