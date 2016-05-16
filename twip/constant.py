#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Constants and discovered values like the path to the current installation folder for the twip package
"""
from __future__ import division, print_function, absolute_import

import os

import pandas as pd

from pug.nlp.util import mkdir_p
import twip

np = pd.np

BASE_PATH = os.path.abspath(os.path.dirname(twip.__file__))
DATA_PATH = os.path.abspath(os.path.join(BASE_PATH, '..', 'data'))
mkdir_p(DATA_PATH)
