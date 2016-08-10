from __future__ import division, print_function, absolute_import, unicode_literals
from builtins import str

import os
from decimal import Decimal
from traceback import print_exc

import pandas as pd


import gzip
import matplotlib

# for ipython notebooks
from IPython.display import display, HTML


DATA_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..', 'Data'))
