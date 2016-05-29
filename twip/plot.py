#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Plot functions like scatter_matrix and double-histograms"""
from __future__ import print_function, division
# from past.builtins import basestring

import json
import os
import logging
from collections import Mapping
from itertools import product
import datetime

import pandas as pd
from pandas.tools.plotting import scatter_matrix
from matplotlib import pyplot as plt

from twip.constant import DATA_PATH, IMAGES_PATH

log = logging.getLogger(__name__)
np = pd.np


def is_quantized(x, N=1000, distinct=0.1):
    if isinstance(x, pd.DataFrame):
        return [is_quantized(x[c]) for c in x.columns]
    elif isinstance(x, np.ndarrayclass_or_type_or_tuple):
        if len(x.shape) == 1:
            return is_quantized(np.array(x))
        else:
            return [is_quantized(row) for row in x]
    else:
        N = min(N, len(x)) or len(x)
        if distinct <= 1:
            distinct = distinct * N
        M = len(set(x[:N]))
        if M <= distinct:
            return True
        else:
            return False


def num_digits(x):
    """Number of digits required to display an integer value
    >>> num_digits(1000)
    4
    >>> num_digits(999)
    3
    >>> num_digits(0)
    1
    >>> num_digits(-1)
    1
    """
    return int(np.math.log((abs(x) * 1.0000000000001 or 1), 10)) + 1


def compose_suffix(num_docs=0, num_topics=0, suffix=None):
    """Create a short, informative, but not-so-unique identifying string for a trained model
    If a str suffix is provided then just pass it through.
    >>> compose_suffix(num_docs=100, num_topics=20)
    '_100X20'
    >>> compose_suffix(suffix='_sfx')
    '_sfx'
    >>> compose_suffix(suffix='')
    ''
    >>> compose_suffix(suffix=None)
    '_0X0'
    """
    if not isinstance(suffix, basestring):
        suffix = '_{}X{}'.format(num_docs, num_topics)
    return suffix

def scatmat(df, category=None, colors='rgob',
            num_plots=4, num_topics=100, num_columns=4,
            show=False, block=False, data_path=DATA_PATH, save=False, verbose=1):
    """FIXME: empty plots that dont go away, Plot and/save scatter matrix in groups of num_columns topics"""

    if category is None:
        category = list(df.columns)[-1]
    if category in df.columns:
        category = df[category]
    else:
        category = pd.Series(category)

    suffix = compose_suffix(len(df), num_topics, save)
    save = bool(save)
    for i in range(min(num_plots * num_columns, num_topics) / num_plots):
        scatter_matrix(df[df.columns[i * num_columns:(i + 1) * num_columns]],
                       marker='+', c=[colors[int(x) % len(colors)] for x in category.values],
                       figsize=(18, 12))
        if save:
            name = 'scatmat_topics_{}-{}.jpg'.format(i * num_columns, (i + 1) * num_columns) + suffix
            plt.savefig(os.path.join(data_path, name + '.jpg'))
        if show:
            if block:
                plt.show()
            else:
                plt.show(block=False)


def summarize_topics(f='lsi_topics.json', num_topics=1000, num_tokens=10, column_width=10, do_print=True, justify=True, data_path=DATA_PATH):
    """Load json file containing topic key/value pairs and print the top m words for the top n features"""
    if isinstance(f, basestring):
        if os.path.sep not in f:
            f = os.path.expanduser(os.path.join(data_path, f))
        f = open(f, 'rUb')
    if isinstance(f, pd.DataFrame):
        f = list(np.array(f[f.columns[-1]]))
    elif isinstance(f, file):
        f = json.load(f)
    if isinstance(f, Mapping):
        f = [v for k, v in sorted(f.items())]
    topics = list(f)
    s = ''
    digits = num_digits(min(len(topics), num_topics) - 1)
    for i, t in enumerate(topics):
        if i > num_topics:
            break
        t_sorted = sorted(t.items(), key=lambda x: -abs(x[1]))[:num_tokens]
        line = '{:{}d}: {}'.format(i, digits, ' '.join(('-+'[int(v > 0)] + '{:{}s}'.format(k[:column_width], column_width) for (k, v) in t_sorted)))
        if not justify:
            line = ' '.join([col for col in line.split(' \t') if col])
        s += line + '\n'
    if do_print:
        print(s)
    return s.split('\n')[:-1]  # get rid of last empty string for last newline


def df_from_groups(groups, columns=None):
    """Create DataFrame of GroupBy object with columns for each product(grouped_value, column_label)"""
    if columns is None:
        columns = list(groups.get_group(groups.indices.keys()[0]).columns)
    df = pd.DataFrame()
    for col, group_label in product(columns, groups.indices.keys()):
        label = '{}_{}'.format(col, group_label)
        df[label] = pd.Series(groups.get_group(group_label)[col].values)
    return df


def groups_from_scores(df, groupby='dustin', threshold=0.7):
    if groupby is None:
        for col in reversed(df.columns):
            if is_quantized(df[col]):
                break
        groupby = col
    if threshold is not None:
        df.ix[df[groupby] < threshold, groupby] = 0
        df.ix[df[groupby] >= threshold, groupby] = 1
    return df.groupby(groupby)


def score_hist(df, columns=None, groupby='dustin', threshold=0.7, stacked=True,
               bins=20, percent=True, alpha=0.33, show=True, block=False, save=False):
    """Plot multiple histograms on one plot, typically of "score" values between 0 and 1
    Typically the groupby or columns of the dataframe are the classification categories (0, .5, 1)
    And the values are scores between 0 and 1.
    """
    df = df if columns is None else df[([] if groupby is None else [groupby]) + list(columns)].copy()
    if groupby is not None or threshold is not None:
        df = groups_from_scores(df, groupby=groupby, threshold=threshold)
    percent = 100. if percent else 1.
    if isinstance(df, pd.core.groupby.DataFrameGroupBy):
        df = df_from_groups(df, columns=columns) * percent
    columns = df.columns if columns is None else columns
    if bins is None:
        bins = 20
    if isinstance(bins, int):
        bins = np.linspace(np.min(df.min()), np.max(df.max()), bins)
    log.debug('bins: {}'.format(bins))
    figs = []

    df.plot(kind='hist', alpha=alpha, stacked=stacked, bins=bins)
    # for col in df.columns:
    #     series = df[col] * percent
    #     log.debug('{}'.format(series))
    #     figs.append(plt.hist(series, bins=bins, alpha=alpha,
    #                 weights=percent * np.ones_like(series) / len(series.dropna()),
    #                 label=stringify(col)))
    plt.legend()
    plt.xlabel('Score (%)')
    plt.ylabel('Percent')
    plt.title('{} Scores for {}'.format(np.sum(df.count()), columns))
    plt.draw()
    if save or not show:
        fig = plt.gcf()
        today = datetime.datetime.today()
        fig.savefig(os.path.join(IMAGES_PATH, 'score_hist_{:04d}-{:02d}-{:02d}_{:02d}{:02d}.jpg'.format(*today.timetuple())))
    if show:
        plt.show(block=block)
    return figs

