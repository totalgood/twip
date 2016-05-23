"""
>>> import Tokenizer
>>> tokenizer = Tokenizer(ngrams=2, lower=True, nonwords_set=set(['hello', 'and']))

>>> from Collections import Counter
>>> list(tokenizer('Hello World again and again?'))
['world', 'again', 'again', 'world again', 'again again']
>>> Counter(tokenizer('Hello World again and again?'))
Counter({'again': 2, 'world': 1, 'again again': 1, 'world again': 1})
>>> x = _
>>> Counter(tokenizer('Hi world once again.'))
Counter({'again': 1, 'world once': 1, 'hi': 1, 'once again': 1, 'world': 1, 'hi world': 1, 'once': 1})
>>> y = _
>>> sum(x[k]*y[k] for k in x if k in y) / sum(v**2 for v in x.values())**.5 / sum(v**2 for v in y.values())**.5
0.42857142857142855
>>> distance_metric(x, y)
0.28196592805724774
"""

# from collections import Counter
from math import pi, acos


def similarity(x, y):
    return sum(x[k] * y[k] for k in x if k in y) / sum(v**2 for v in x.values())**.5 / sum(v**2 for v in y.values())**.5


def distance_metric(x, y):
    return 1 - 2 * acos(similarity(x, y)) / pi
