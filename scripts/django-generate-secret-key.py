r"""Pseudo-random django secret key generator.

WARNING: prints SECRET_KEY to terminal which many consider unsafe.
"""
from __future__ import print_function, division, absolute_import, unicode_literals

import string
import random

# Get ascii (or unicode) characters numbers and punctuation (minus quote characters as they could terminate string).
chars = ''.join([string.ascii_letters, string.digits, string.punctuation]).replace('\'', '').replace('"', '').replace('\\', '')

SECRET_KEY = ''.join([random.SystemRandom().choice(chars) for i in range(50)])

print(SECRET_KEY)