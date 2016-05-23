#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Load cleaned tweets and add additional columns for NLP features

- Counter dict of words (sparse word vector)
- Freq dict (sparse TFIDF)
- Num words
- Num characters
"""
from __future__ import division, print_function, absolute_import
# from past.builtins import basestring

import os
from collections import Counter

import pandas as pd
import progressbar

# you really want to be efficient about RAM, so user iter and itertools
# from itertools import izip
from twip.constant import DATA_PATH
from pug.nlp.segmentation import Tokenizer
# from pug.nlp.constant import MAX_UINT16

np = pd.np


segment_words = Tokenizer(ngrams=1, lower=True)


def tf_df(df, num_tweets=1000000, verbosity=1, min_freq=2, max_freq=.9):
    if verbosity > 0:
        print('Compiling a vocabulary from the tokens found in {} tweets'.format(len(df)))
        pbar_i = 0
        pbar = progressbar.ProgressBar(maxval=min(df.shape[0], num_tweets) + 1)
        pbar.start()
    termfreq = Counter()
    docfreq = Counter()
    for twid, row in df.iterrows():
        if verbosity:
            pbar_i += 1
            pbar.update(pbar_i)
        if pbar_i > num_tweets:
            break
        text = row.text if isinstance(row.text, basestring) and row.text else ''
        counts = Counter(segment_words(text))
        termfreq = termfreq + counts
        docfreq = docfreq + Counter(counts.keys())
    if verbosity > 0:
        pbar.finish()
        print('Found {} unique tokens'.format(len(termfreq)))
    tfdf = pd.DataFrame()
    tfdf['tf'] = pd.Series(termfreq, name='tf')
    tfdf['df'] = pd.Series(docfreq, name='df')
    mask = (tfdf.df >= min_freq) & (tfdf.df <= int(max_freq * len(df)))
    tfdf = tfdf[mask]
    # FIXME: filter tfdf for extremely frequent (functional words) and infrequent words (URLs, userIDs)
    return tfdf


def count_words(df, tfdf=None, num_tweets=1000000, verbosity=1):
    if tfdf is None:
        tfdf = tf_df(df, num_tweets=num_tweets, verbosity=verbosity)
    if verbosity > 0:
        pbar_i = 0
        pbar = progressbar.ProgressBar(maxval=min(df.shape[0], num_tweets) + 1)
        pbar.start()
    counts = pd.DataFrame(np.zeros((len(tfdf), len(df)), dtype='uint16'), index=tfdf.index, columns=df.index)
    stats = []
    for twid, row in df.iterrows():
        if verbosity:
            pbar_i += 1
            pbar.update(pbar_i)
        if pbar_i > num_tweets:
            break
        text = row.text if isinstance(row.text, basestring) and row.text else ''
        counts[twid] = pd.Series(Counter(segment_words(text)), name=twid, dtype='uint16')
        # counts = pd.concat([counts, pd.Series(Counter(segment_words(text)), name=twid)], axis=1)
        stats += [[counts[twid].sum(), np.sum(np.array(counts[twid] > 0)), len(text)]]
    if verbosity > 0:
        pbar.finish()
    stats = pd.DataFrame(stats, index=df.index[:len(stats)], columns=['text_num_words', 'text_num_unique', 'text_len'])
    df = pd.concat([df.iloc[:num_tweets], stats], axis=1)
    if verbosity:
        pbar.finish()
    return df, counts.T


def run(num_tweets=1000000, verbosity=1):
    print('Loading previously cleaned tweets...')
    # the round-trip to disk cleans up encoding issues so encoding option no longer needs to be specified and gzip 
    df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), index_col='id', compression='gzip',
                      quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
    print('Found {} tweets.'.format(len(df)))
    print('Loading previously compiled vocab...')
    # the round-trip to disk cleans up encoding issues so encoding option no longer needs to be specified and gzip 
    try:
        tfdf = pd.read_csv(os.path.join(DATA_PATH, 'tweet_vocab.csv.gz'), index_col=0, compression='gzip',
                          quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
        assert(len(tfdf) > 10000)
    except:
        tfdf = tf_df(df, num_tweets=num_tweets, verbosity=verbosity)
        tfdf.to_csv(os.path.join(DATA_PATH, 'tweet_vocab.csv.gz'), compression='gzip',
                    quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    df, counts = count_words(df, tfdf=tfdf, num_tweets=num_tweets, verbosity=verbosity)
    df.to_csv(os.path.join(DATA_PATH, 'counted_tweets.csv.gz'), compression='gzip',
              quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    counts = counts.T  # word vectors in rows instead of columns
    counts.to_csv(os.path.join(DATA_PATH, 'tweet_word_vectors.csv.gz'), compression='gzip',
                  quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    return df, counts
