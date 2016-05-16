"""Tokenization and string processing to support NLP"""
from __future__ import division, print_function, absolute_import
# `pip install future` for universal python2/3
from past.builtins import basestring

import re
from itertools import chain
import subprocess
from collections import Counter

import nltk
import pandas as pd
np = pd.np

from twip.constant import FINANCIAL_WHITESPACE, PERCENT_SYMBOLS, FINANCIAL_MAPPING, DATE_TYPES
from twip.constant import NULL_VALUES, NULL_REPR_VALUES, MAX_NULL_REPR_LEN
from twip.regex import RE_NONWORD, CRE_TOKEN, CRE_BAD_FILENAME, CRE_WHITESPACE
from twip.serial import PrettyDict, stringify, passthrough
from twip.numeric import safe_log

STEMMER_DATASETS = {'snowball': 'udhr', 'wordnet': 'wordnet'}
STEMMER_TYPES = {
    'lancaster': nltk.stem.LancasterStemmer,
    'porter': nltk.stem.PorterStemmer,
    'snowball': nltk.stem.SnowballStemmer,
    'wordnet': nltk.stem.WordNetLemmatizer,
    }


def generate_tokens(doc, regex=CRE_TOKEN, strip=True, nonwords=False):
    r"""Return a sequence of words or tokens, using a re.match iteratively through the str

    >>> doc = "John D. Rock\n\nObjective: \n\tSeeking a position as Software --Architect-- / _Project Lead_ that can utilize my expertise and"
    >>> doc += " experiences in business application development and proven records in delivering 90's software. \n\nSummary: \n\tSoftware Architect"
    >>> doc += " who has gone through several full product-delivery life cycles from requirements gathering to deployment / production, and"
    >>> doc += " skilled in all areas of software development from client-side JavaScript to database modeling. With strong experiences in:"
    >>> doc += " \n\tRequirements gathering and analysis."
    >>> len(list(generate_tokens(doc, strip=False, nonwords=True)))
    82
    >>> seq = list(generate_tokens(doc, strip=False, nonwords=False))
    >>> len(seq)
    70
    >>> '.' in seq or ':' in seq
    False
    >>> s = set(generate_tokens(doc, strip=False, nonwords=True))
    >>> all(t in s for t in ('D', '.', ':', '_Project', 'Lead_', "90's", "Architect", "product-delivery"))
    True
    """
    if isinstance(regex, basestring):
        regex = re.compile(regex)
    for w in regex.finditer(doc):
        if w:
            w = w.group()
            if strip:
                w = w.strip(r'-_*`()}{' + r"'")
            if w and (nonwords or not re.match(r'^' + RE_NONWORD + '$', w)):
                yield w


def financial_float(s, scale_factor=1, typ=float,
                    ignore=FINANCIAL_WHITESPACE,
                    percent_str=PERCENT_SYMBOLS,
                    replace=FINANCIAL_MAPPING,
                    normalize_case=str.lower):
    """Strip dollar signs and commas from financial numerical string

    Also, convert percentages to fractions/factors (generally between 0 and 1.0)

    >>> [financial_float(x) for x in ("12k Flat", "12,000 flat", "20%", "$10,000 Flat", "15K flat", "null", "None", "", None)]
    [12000.0, 12000.0, 0.2, 10000.0, 15000.0, 'null', 'none', '', None]
    """
    percent_scale_factor = 1
    if isinstance(s, basestring):
        s = normalize_case(s).strip()
        for i in ignore:
            s = s.replace(normalize_case(i), '')
        s = s.strip()
        for old, new in replace:
            s = s.replace(old, new)
        for p in percent_str:
            if s.endswith(p):
                # %% will become 0.0001
                percent_scale_factor *= 0.01
                s = s[:-len(p)]
    try:
        return (scale_factor if scale_factor < 1 else percent_scale_factor) * typ(float(s))
    except (ValueError, TypeError):
        return s


def friendly(obj):
    """Make the representation of an object (mainly numbers) more human friendly

    >>> friendly(1e6)
    '1M'
    >>> friendly(-1e3)
    '-1k'
    >>> friendly(1.23456789e9)
    '1.23G'
    >>> friendly(0)
    '0'
    >>> friendly('whatever')
    'whatever'
    """
    powers = 'TGMk munp'
    if isinstance(obj, (float, int, long)):
        sign = 1 - 2 * int(obj < 0)
        obj = abs(obj)
        i = 0
        mid = 4
        while np.inf > safe_log(obj, 1000) >= .9999999 and i <= mid and obj > 0 and np.isfinite(obj):
            obj = obj * .001
            i += 1
        while np.inf > safe_log(obj, 1000) < -.25 and i > mid - len(powers) and obj > 0 and np.isfinite(obj):
            obj = obj * 1000.
            i -= 1
        return '{:.3g}{}'.format(sign * obj, powers[mid - i] if i else '')
    return stringify(obj)


def is_invalid_date(d):
    """Return boolean to indicate whether date is invalid, None if valid, False if not a date

    >>> import datetime
    >>> is_invalid_date(datetime.datetime(1970, 1, 1, 0, 0, 1))
    >>> is_invalid_date(datetime.datetime(1970, 1, 1))
    >>> is_invalid_date(datetime.datetime(1969, 12, 31, 23, 59, 59, 999999))
    True
    >>> is_invalid_date(datetime.date(2100, 1, 1))
    True
    >>> is_invalid_date(datetime.datetime(2099, 12, 31, 23, 59, 59))
    >>> [is_invalid_date(x) for x in (None, 0, 1.0, '2000-01-01')]
    [False, False, False, False]
    """
    if not isinstance(d, DATE_TYPES):
        return False
    if d.year < 1970 or d.year >= 2100:
        return True


def nonnull_fields(obj, pretty=True):
    """Generate `.values()` dict from a table record, removing non-informative values

    Noninformative values include:
      date < 1970
      date > 2100
      False
      None
      0
      0.0
      '0'
      '0.0'
      '0.0000'
    """
    return PrettyDict((k, v) for k, v in [(f.attname, getattr(obj, f.attname, None))
                for f in obj._meta.fields] if (
                    v and
                    v not in NULL_VALUES and
                    stringify(v).strip().lower()[:MAX_NULL_REPR_LEN] not in NULL_REPR_VALUES and
                    not is_invalid_date(v)))


def nltk_download(name, ignore_errors=True):
    r"""Like nltk.download, but be quiet about it, and get a room (separate python process)

    Does some simple whitespace normalization on `name`, but doesn't yet do fuzzy matching
    Caches the normalized names of packages already attempted, so they aren't re-tried

    >>> nltk_download('nonexistent dataset name', ignore_errors=True)
    False
    >>> nltk_download('WordNet', ignore_errors=True)
    True
    >>> nltk_download('wordnet', ignore_errors=True)
    True
    """
    name = re.sub(r"[-\s=+']+", '_', name.lower())
    if name in nltk_download.done:
        return nltk_download.done[name]
    proc = subprocess.Popen(["python", "-c", "import nltk; nltk.download('{}')".format(name)], stdout=subprocess.PIPE)
    msgs = [s for s in proc.communicate() if s is not None]
    if any(re.match(r'^\[nltk_data\]\s+Error', msg, flags=re.IGNORECASE) for msg in msgs):
        nltk_download.done[name] = False
        if ignore_errors:
            return nltk_download.done[name]
        raise ValueError('Unable to download the requested NLTK dataset: {}'.format('\n'.join(msgs)))
    nltk_download.done[name] = True
    return nltk_download.done[name]
nltk_download.done = dict()


class PassthroughStemmer(nltk.stem.StemmerI):
    """Dummy passthrough stemmer. Override or monkey-patch the stem method.

    Instances works as both a function and a normal StemmerI instance with a stem() method.

    >>> PassthroughStemmer().stem('Running')
    'Running'
    """
    def stem(self, s):
        return s

    def __call__(self, s):
        return self.stem(s)


class Stemmer(PassthroughStemmer):

    def __init__(self, stemmer=None):
        """Implement the nltk.stem.StemmerI interface and defaults to "passthrough" stemming

        Implements a `stem()` method which transcodes a string (typically a token or n-gram).

        Arguments:
          stemmer (function or nltk.stem.StemmerI or None): Indicate the stemmer to use.
        >>> Stemmer().stem('Running')
        'Running'
        """

        if stemmer is True:
            self._stemmer = nltk.stem.LancasterStemmer()
            self.stem = self._stemmer.stem
        elif hasattr(stemmer, 'stem') and callable(stemmer.stem):
            self._stemmer = stemmer
            self.stem = self._stemmer.stem
        elif hasattr(stemmer, 'lemmatize') and callable(stemmer.lemmatize):
            self._stemmer = stemmer
            # this may produce an unpicklable bound method
            self.stem = self._stemmer.lemmatize
        else:
            super(Stemmer, self).__init__()
            self._stemmer = None

    def stem(self, s):
        """This should make the Stemmer picklable and unpicklable by not using bound methods"""
        if self._stemmer is None:
            return passthrough(s)
        try:
            # try the local attribute `stemmer`, a StemmerI instance first
            # if you use the self.stem method from an unpickled object it may not work
            return getattr(getattr(self, '_stemmer', None), 'stem', None)(s)
        except (AttributeError, TypeError):
            return getattr(getattr(self, '_stemmer', self), 'lemmatize', passthrough)(s)


def make_stemmer(stem=None, min_len=3):
    """Build a nltk.stem.StemmerI instance from regex, named stemmer ('Lancaster', 'Porter', None), or function

    Arguments:
      min (int): Dont stem anything short than this. e.g. for min=4 don't stem token "I'm" to "I"

    >>> make_stemmer()
    <Stemmer object at ...>
    >>> make_stemmer(str_lower)
    <function str_lower at ...>
    >>> make_stemmer('str_lower')
    <function str_lower at ...>
    >>> make_stemmer('Lancaster')
    <Stemmer object at ...>
    >>> make_stemmer('WordNet')
    <Stemmer object at ...>
    >>> make_stemmer('ing$|s$')
    <Stemmer object at ...>
    """
    if not stem or stem == 'passthrough':
        stem = Stemmer()
        # FIXME: this is unnecessary?! and will make the object less picklable?
        stem.stem = passthrough
        return stem
    if isinstance(stem, basestring):
        stem = globals().get(stem, None) or locals().get(stem, stem)
    # in case stem is a compiled stemmer regex, make it a string so it can be compiled by the nltk.RegexStemmer
    if hasattr(stem, 'pattern'):
        stem = Stemmer(nltk.stem.RegexpStemmer(stem, min=min_len))
    if isinstance(stem, basestring):
        # strip nonascii and whitespace, and only consider first letter, case-insentively
        name = stringify(stem).lower().strip() or 'porter'
        if name in STEMMER_TYPES:
            dataset = STEMMER_DATASETS.get(name, None)
            if dataset is not None:
                nltk_download(dataset)
            stem = STEMMER_TYPES.get(name, stem)
        else:
            stem = Stemmer(nltk.stem.RegexpStemmer(stem, min=min_len))
    if isinstance(stem, type):
        stem = stem()
    if (hasattr(stem, 'stem') and callable(stem.stem)) or (hasattr(stem, 'lemmatize') and callable(stem.lemmatize) or stem is True):
        return Stemmer(stem)
    elif callable(stem):
        return stem
    raise(ValueError("Unable to make {} into a stemmer. ".format(stem) +
                     "Try 'porter', 'lancaster', None, a regular expression, a callable function, " +
                     "or an object with a stem method."))


def make_named_stemmer(stem=None, min_len=3):
    """Construct a callable object and a string sufficient to reconstruct it later (unpickling)

    >>> make_named_stemmer('str_lower')
    ('str_lower', <function str_lower at ...>)
    >>> make_named_stemmer('Lancaster')
    ('lancaster', <Stemmer object at ...>)
    """
    name, stem = stringify(stem), make_stemmer(stem=stem, min_len=min_len)
    if hasattr(stem, '__name__'):
        return stem.__name__, stem
    if name.strip().lower() in STEMMER_TYPES:
        return name.strip().lower(), stem
    if hasattr(stem, 'pattern'):
        return stem.pattern, stem
    return stringify(stem), stem


def vocab_freq(docs, limit=1e6, verbose=1, tokenizer=generate_tokens):
    """Get the set of words used anywhere in a sequence of documents and count occurrences

    >>> gen = ('label: ' + chr(ord('A') + i % 3)*3 for i in range(11))
    >>> vocab_freq(gen, verbose=0)
    Counter({'label': 11, 'AAA': 4, 'BBB': 4, 'CCC': 3})
    """
    total = Counter()
    try:
        limit = min(limit, docs.count())
        docs = docs.iterator()
    except:
        pass
    for i, doc in enumerate(docs):
        try:
            doc = doc.values()
        except AttributeError:
            if not isinstance(doc, basestring):
                doc = ' '.join([stringify(v) for v in doc])
            else:
                doc = stringify(doc)
        if i >= limit:
            break
        c = Counter(tokenizer(doc, strip=True, nonwords=False))
        if verbose and (verbose < 1e-3 or not i % int(limit * verbose)):
            print('{}: {} ... {}'.format(i, c.keys()[:3], c.keys()[-3:] if len(c.keys()) > 6 else ''))
        total += c
    return total


### BROKEN
# from itertools import izip


# def gen_ngrams(token_seq, n=1, join=' '):
#     """Return a list of n-tuples, one for each possible sequence of n items in the token_list

#     Arguments:
#       join (bool or str): if str, then join ngrom tuples on it before returning
#          True is equivalent to join=' '
#          default = True

#     See: http://stackoverflow.com/a/30609050/623735

#     >>> list(gen_ngrams('goodbye cruel world'.split(), join=False))
#     [('goodbye',), ('cruel',), ('world',)]
#     >>> list(gen_ngrams('goodbye cruel world'.split(), 2, join=False))
#     [('goodbye', 'cruel'), ('cruel', 'world')]
#     >>> list(gen_ngrams('goodbye cruel world'.split(), 2, join='*'))
#     ['goodbye*cruel', 'cruel*world']
#     """
#     join = ' ' if join is True else join
#     print('called with token_seq={}, n={}'.format(token_seq, n))
#     if isinstance(join, basestring):
#         for k, ngram in enumerate(join.join(ng) for ng in gen_ngrams(token_seq, n=n, join=False)):
#             print('join #{}, ngram={}'.format(k, ngram))
#             yield ngram
#     else:
#         for j, ngram in enumerate(zip(*[[tok for j, tok in enumerate(token_seq) if j >= i] for i in range(n)])):
#             print('ngram #{}, ngram={}'.format(j, ngram))
#             yield ngram
#         # for ngram in izip(*((tok for j, tok in enumerate(token_seq) if j >= i) for i in xrange(n))):
#         #     yield ngram


def make_filename(s, allow_whitespace=False, allow_underscore=False, allow_hyphen=False, limit=255, lower=False):
    r"""Make sure the provided string is a valid filename, and optionally remove whitespace

    >>> make_filename('Not so great!')
    'Notsogreat'
    >>> make_filename('')
    'empty'
    >>> make_filename('EOF\x00 EOL\n')
    'EOFEOL'
    >>> make_filename('EOF\x00 EOL\n', allow_whitespace=True)
    'EOF EOL\n'
    """
    s = stringify(s)
    s = CRE_BAD_FILENAME.sub('', s)
    if not allow_whitespace:
        s = CRE_WHITESPACE.sub('', s)
    if lower:
        s = str.lower(s)
    if not allow_hyphen:
        s = s.replace('-', '')
    if not allow_underscore:
        s = s.replace('_', '')
    if limit is not None:
        s = s[:limit]
    return s or 'empty'[:limit]
