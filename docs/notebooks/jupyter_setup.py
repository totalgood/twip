# coding: utf-8
from __future__ import division, print_function, absolute_import
from past.builtins import basestring  #noqa

import matplotlib
get_ipython().magic(u'matplotlib inline')
from IPython.display import display, HTML 

import os
from decimal import Decimal
from traceback import print_exc

import pandas as pd
import pandas_profiling

# you really want to be efficient about RAM, so user iter and itertools
# from itertools import izip
from twip.constant import DATA_PATH
from pug.nlp.util import dict2obj

display(HTML("<style>.container { width:100% !important; }</style>"))
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 500)