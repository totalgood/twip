#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constants and discovered values like the path to the current installation folder for the twip package
"""
from __future__ import division, print_function, absolute_import, unicode_literals
# from future.utils import viewitems  # noqa
# from builtins import str  # noqa
# from past.builtins import basestring  # noqa

# try:
#     from itertools import izip as zip
# except ImportError:
#     pass

import os

import pandas as pd

from twip.futil import mkdir_p

from matplotlib import get_backend
from matplotlib import use as set_backend

os.environ['QT_API'] = 'pyside'
DEFAULT_MPL_BACKEND = get_backend()

try:
    import PyQt4  # noqa
    assert(PyQt4)
    set_backend('Qt4Agg')
    from matplotlib import pyplot as plt
except ImportError:
    try:
        set_backend(DEFAULT_MPL_BACKEND)
        from matplotlib import pyplot as plt
    except ImportError:
        set_backend('TkAgg')
        from matplotlib import pyplot as plt
try:
    plt.style.use('ggplot')
except:  # AttributeError:
    print('Matplotlib needs to be upgraded to >= 1.4.1 to enable CSS styling and prettier plots.')

np = pd.np

BASE_PATH = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
DATA_PATH = os.path.abspath(os.path.join(BASE_PATH, '..', 'data'))
DOCS_PATH = os.path.abspath(os.path.join(BASE_PATH, '..', 'docs'))
IMAGES_PATH = os.path.abspath(os.path.join(DOCS_PATH, 'images'))

mkdir_p(DATA_PATH)
