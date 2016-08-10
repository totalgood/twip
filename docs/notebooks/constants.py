#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constants and discovered values, like path to current installation of pug-nlp."""
from __future__ import division, print_function, absolute_import, unicode_literals
from builtins import str

import os
import string
import datetime
import collections

import pandas as pd

np = pd.np
BASE_PATH = os.path.dirname(__file__)
DATA_PATH = os.path.join(BASE_PATH, '..', 'Data')

tld_iana = pd.read_csv(os.path.join(DATA_PATH, 'tlds-from-iana.csv'))
tld_iana = collections.OrderedDict(sorted(zip((tld.strip().lstrip('.') for tld in tld_iana.domain),
                                              [(sponsor.strip(), -1) for sponsor in tld_iana.sponsor]),
                                          key=lambda x: len(x[0]),
                                          reverse=True))
# top 20 in Google searches per day
# sorted by longest first so .com matches before .om (Oman)
tld_popular = collections.OrderedDict(sorted([
    ('com', ('Commercial', 4860000000)),
    ('org', ('Noncommercial', 1950000000)),
    ('edu', ('US accredited postsecondary institutions', 1550000000)),
    ('gov', ('United States Government', 1060000000)),
    ('uk',  ('United Kingdom', 473000000)),
    ('net', ('Network services', 206000000)),
    ('ca', ('Canada', 165000000)),
    ('de', ('Germany', 145000000)),
    ('jp', ('Japan', 139000000)),
    ('fr', ('France', 96700000)),
    ('au', ('Australia', 91000000)),
    ('us', ('United States', 68300000)),
    ('ru', ('Russian Federation', 67900000)),
    ('ch', ('Switzerland', 62100000)),
    ('it', ('Italy', 55200000)),
    ('nl', ('Netherlands', 45700000)),
    ('se', ('Sweden', 39000000)),
    ('no', ('Norway', 32300000)),
    ('es', ('Spain', 31000000)),
    ('mil', ('US Military', 28400000)),
    ], key=lambda x: len(x[0]), reverse=True))

uri_schemes_iana = sorted(pd.read_csv(os.path.join(DATA_PATH, 'uri-schemes.xhtml.csv'),
                                      index_col=0).index.values,
                          key=lambda x: len(str(x)), reverse=True)
uri_schemes_popular = ['chrome-extension', 'example', 'content', 'bitcoin',
                       'telnet', 'mailto',
                       'https', 'gtalk',
                       'http', 'smtp', 'feed',
                       'udp', 'ftp', 'ssh', 'git', 'apt', 'svn', 'cvs']

# these may not all be the sames isinstance types, depending on the env
FLOAT_TYPES = (float, np.float16, np.float32, np.float64, np.float128)
FLOAT_DTYPES = tuple(set(np.dtype(typ) for typ in FLOAT_TYPES))
INT_TYPES = (int, long, np.int0, np.int8, np.int16, np.int32, np.int64)
INT_DTYPES = tuple(set(np.dtype(typ) for typ in INT_TYPES))
NUMERIC_TYPES = tuple(set(list(FLOAT_TYPES) + list(INT_TYPES)))
NUMERIC_DTYPES = tuple(set(np.dtype(typ) for typ in NUMERIC_TYPES))

DATETIME_TYPES = (datetime.datetime, pd.datetime, np.datetime64)
DATE_TYPES = (datetime.datetime, datetime.date)

# matrices can be column or row vectors if they have a single col/row
VECTOR_TYPES = (list, tuple, np.matrix, np.ndarray)
MAPPING_TYPES = (collections.Mapping, pd.Series, pd.DataFrame)

# These are the valid dates for all 3 datetime types in python (and the underelying integer nanoseconds)
MAX_INT64 = 9223372036854775807
MAX_UINT64 = MAX_INT64 * 2 - 1
MAX_UINT32 = 4294967295
MAX_INT32 = MAX_UINT32 // 2
MAX_UINT16 = 65535
MAX_INT16 = 32767
MAX_TIMESTAMP = pd.tslib.Timestamp('2262-04-11 23:47:16.854775807', tz='utc')
MIN_TIMESTAMP = pd.tslib.Timestamp(pd.datetime(1677, 9, 22, 0, 12, 44), tz='utc')
ZERO_TIMESTAMP = pd.tslib.Timestamp('1970-01-01 00:00:00', tz='utc')
MIN_DATETIME = MIN_TIMESTAMP.to_datetime()
MAX_DATETIME = MAX_TIMESTAMP.to_datetime()
MIN_DATETIME64 = MIN_TIMESTAMP.to_datetime64()
MAX_DATETIME64 = MAX_TIMESTAMP.to_datetime64()
INF = pd.np.inf
NAN = pd.np.nan
NAT = pd.NaT

# str constants
MAX_CHR = MAX_CHAR = chr(127)
APOSTROPHE_CHARS = "'`’"
UNPRINTABLE = ''.join(set(chr(i) for i in range(128)) - set(string.printable))
string.unprintable = UNPRINTABLE  # monkey patch so import string from this module if you want this!

NULL_VALUES = set(['0', 'None', 'null', "'"] + ['0.' + z for z in ['0' * i for i in range(10)]])
# if datetime's are 'repr'ed before being checked for null values sometime 1899-12-30 will come up
NULL_REPR_VALUES = set(['datetime.datetime(1899, 12, 30'])
# to allow NULL checks to strip off hour/min/sec from string repr when checking for equality
MAX_NULL_REPR_LEN = max(len(s) for s in NULL_REPR_VALUES)

PERCENT_SYMBOLS = ('percent', 'pct', 'pcnt', 'pt', r'%')
FINANCIAL_WHITESPACE = ('Flat', 'flat', ' ', ',', '"', "'", '\t', '\n', '\r', '$')
FINANCIAL_MAPPING = (('k', '000'), ('M', '000000'))
