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

np = pd.np


segment_words = Tokenizer(ngrams=1, lower=True)


def count_words(df, num_tweets=1000000, verbosity=1):
    if verbosity > 0:
        pbar_i = 0
        pbar = progressbar.ProgressBar(maxval=df.shape[0])
        pbar.start()

    counts = pd.DataFrame(columns=df.index)
    stats = []
    for twid, row in df.iterrows():
        if verbosity:
            pbar_i += 1
            pbar.update(pbar_i)
        if pbar_i > num_tweets:
            break
        text = row.text if isinstance(row.text, basestring) and row.text and not isinstance(row.text, np.nan) else ''
        counts[twid] = pd.Series(Counter(segment_words(text)))
        stats += [[counts[twid].sum(), np.sum(np.array(counts[twid] > 0)), len(text)]]
    stats = pd.DataFrame(stats, index=df.index, columns=['text_num_words', 'text_num_unique', 'text_len'])
    df = pd.concat([df, stats], axis=1)
    if verbosity:
        pbar.finish()
    return df, counts


def run():
    print('Loading previously cleaned tweets...')
    # the round-trip to disk cleans up encoding issues so encoding option no longer needs to be specified and gzip 
    df = pd.read_csv(os.path.join(DATA_PATH, 'cleaned_tweets.csv.gz'), index_col='id', compression='gzip',
                      quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC, low_memory=False)
    print('Found {} tweets.'.format(len(df)))
    df, counts = count_words(df)
    df.to_csv(os.path.join(DATA_PATH, 'counted_tweets.csv.gz'), compression='gzip',
              quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
    counts = counts.T  # word vectors in rows instead of columns
    counts.to_csv(os.path.join(DATA_PATH, 'tweet_word_vectors.csv.gz'), compression='gzip',
                    quotechar='"', quoting=pd.io.common.csv.QUOTE_NONNUMERIC)
