from __future__ import division, print_function, absolute_import
# `pip install future` for universal python2/3
from past.builtins import basestring

import re

# import gensim

from twip.regex import RE_TOKEN, RE_NONWORD
from twip.util import str_strip, str_lower, to_ascii, stringify
from twip.nlp import make_named_stemmer

CRE_TOKEN = re.compile(RE_TOKEN)


class Tokenizer(object):
    """Callable and iterable class that yields substrings split on spaces or other configurable delimitters.

    For both __init__ and __call__, doc is the first arg.
    TODO: All args and functionality of __init__() and __call__() should be the same.

    FIXME: Implement the `nltk.tokenize.TokenizerI` interface
           Is it at all pythonic to make a class callable and iterable?
           Is it pythonic to have to instantiate a TokenizerI instance and then call that instance's `tokenize` method?

    >>> abc = (chr(ord('a') + (i % 26)) for i in xrange(1000))
    >>> tokenize = Tokenizer(ngrams=5)
    >>> ans = list(tokenize(' '.join(abc)))
    >>> ans[:7]
    ['a', 'b', 'c', 'd', 'e', 'f', 'g']
    >>> ans[1000:1005]
    ['a b', 'b c', 'c d', 'd e', 'e f']
    >>> ans[1999:2004]
    ['a b c', 'b c d', 'c d e', 'd e f', 'e f g']
    >>> tokenize = Tokenizer(stem='Porter')
    >>> doc = "Here're some stemmable words provided to you for your stemming pleasure."
    >>> sorted(set(tokenize(doc)) - set(Tokenizer(doc, stem='Lancaster')))
    [u"Here'r", u'pleasur', u'some', u'stemmabl', u'your']
    >>> sorted(set(Tokenizer(doc, stem='WordNet')) - set(Tokenizer(doc, stem='Lancaster')))
    ["Here're", 'pleasure', 'provided', 'some', 'stemmable', 'stemming', 'your']
    """
    __safe_for_unpickling__ = True

    def __init__(self, doc=None, regex=CRE_TOKEN, strip=True, nonwords=False, nonwords_set=None, nonwords_regex=RE_NONWORD,
                 lower=None, stem=None, ngrams=1):
        # specific set of characters to strip
        self.strip_chars = None
        if isinstance(strip, basestring):
            self.strip_chars = strip
            # strip_chars takes care of the stripping config, so no need for strip function anymore
            self.strip = None
        elif strip is True:
            self.strip_chars = '-_*`()"' + '"'
        strip = strip or None
        # strip whitespace, overrides strip() method
        self.strip = strip if callable(strip) else (str_strip if strip else None)
        self.doc = to_ascii(doc)
        self.regex = regex
        if isinstance(self.regex, basestring):
            self.regex = re.compile(self.regex)
        self.nonwords = nonwords  # whether to use the default REGEX for nonwords
        self.nonwords_set = nonwords_set or set()
        self.nonwords_regex = nonwords_regex
        self.lower = lower if callable(lower) else (str_lower if lower else None)
        self.stemmer_name, self.stem = make_named_stemmer(stem)  # stem can be a callable Stemmer instance or just a function
        self.ngrams = ngrams or 1  # ngram degree, numger of ngrams per token
        if isinstance(self.nonwords_regex, basestring):
            self.nonwords_regex = re.compile(self.nonwords_regex)
        elif self.nonwords:
            try:
                self.nonwords_set = set(self.nonwords)
            except TypeError:
                self.nonwords_set = set(['None', 'none', 'and', 'but'])
                # if a set of nonwords has been provided dont use the internal nonwords REGEX?
                self.nonwords = not bool(self.nonwords)

    def __call__(self, doc):
        """Lazily tokenize a new document (tokens aren't generated until the class instance is iterated)

        >>> list(Tokenizer()('new string to parse'))
        ['new', 'string', 'to', 'parse']
        """
        # tokenization doesn't happen until you try to iterate through the Tokenizer instance or class
        self.doc = to_ascii(doc)
        # need to return self so that this will work: Tokenizer()('doc (str) to parse even though default doc is None')
        return self
    # to conform to this part of the nltk.tokenize.TokenizerI interface
    tokenize = __call__

    def __reduce__(self):
        """Unpickling constructor and args so that pickling can be done efficiently without any bound methods, etc"""
        return (Tokenizer, (None, self.regex, self.strip, self.nonwords, self.nonwords_set, self.nonwords_regex,
                self.lower, self.stemmer_name, self.ngrams))

    def span_tokenize(self, s):
        """Identify the tokens using integer offsets `(start_i, end_i)` rather than copying them to a new sequence

        The sequence of tokens (strings) can be generated with

            `s[start_i:end_i] for start_i, end_i in span_tokenize(s)`

        Returns:
          generator of 2-tuples of ints, like ((int, int) for token in s)
        """
        return
        # raise NotImplementedError("span_tokenizer interface not yet implemented, so just suck it up and use RAM to tokenize() ;)")

    def tokenize_sents(self, strings):
        """NTLK.
        Apply ``self.tokenize()`` to each element of ``strings``.  I.e.:
            return [self.tokenize(s) for s in strings]
        :rtype: list(list(str))
        """
        return [self.tokenize(s) for s in strings]

    def span_tokenize_sents(self, strings):
        """
        Apply ``self.span_tokenize()`` to each element of ``strings``.  I.e.:
            return iter((self.span_tokenize(s) for s in strings))
        :rtype: iter(list(tuple(int, int)))
        """
        for s in strings:
            yield list(self.span_tokenize(s))

    def __iter__(self, ngrams=None):
        r"""Generate a sequence of words or tokens, using a re.match iteratively through the str

        TODO:
          - need two different self.lower and lemmatize transforms, 1 before and 1 after nonword detection
          - each of 3 nonword filters on a separate line, setting w=None when nonword "hits"
          - refactor `nonwords` arg/attr to `ignore_stopwords` to be more explicit

        >>> doc = "John D. Rock\n\nObjective: \n\tSeeking a position as Software --Architect-- / _Project Lead_ that can utilize my expertise and"
        >>> doc += " experiences in business application development and proven records in delivering 90's software. "
        >>> doc += "\n\nSummary: \n\tSoftware Architect"
        >>> doc += " who has gone through several full product-delivery life cycles from requirements gathering to deployment / production, and"
        >>> doc += " skilled in all areas of software development from client-side JavaScript to database modeling. With strong experiences in:"
        >>> doc += " \n\tRequirements gathering and analysis."

        The python splitter will produce 2 tokens that are only punctuation ("/")
        >>> len([s for s in doc.split() if s])
        72

        The built-in nonword REGEX ignores all-punctuation words, so there are 2 less here:
        >>> len(list(Tokenizer(doc, strip=False, nonwords=False)))
        70

        In addition, punctuation at the end of tokens is stripped so "D. Rock" doesn't tokenize to "D." but rather "D"
        >>> run_together_tokens = ''.join(list(Tokenizer(doc, strip=False, nonwords=False)))
        >>> '/' in run_together_tokens or ':' in ''.join(run_together_tokens)
        False

        But you can turn off stripping when instantiating the object.
        >>> all(t in Tokenizer(doc, strip=False, nonwords=True) for t in ('D', '_Project', 'Lead_', "90's", "product-delivery"))
        True
        """
        ngrams = ngrams or self.ngrams
        # FIXME: Improve memory efficiency by making this ngram tokenizer an actual generator
        if ngrams > 1:
            original_tokens = list(self.__iter__(ngrams=1))
            for tok in original_tokens:
                yield tok
            for i in range(2, ngrams + 1):
                for tok in list_ngrams(original_tokens, n=i, join=' '):
                    yield tok
        else:
            for w in self.regex.finditer(self.doc):
                if w:
                    w = w.group()
                    w = w if not self.strip_chars else str_strip(w, self.strip_chars)
                    w = w if not self.strip else self.strip(w)
                    w = w if not self.stem else self.stem(w)
                    w = w if not self.lemmatize else self.lemmatize(w)
                    w = w if not self.lower else self.lower(w)
                    # FIXME: nonword check before and after preprossing? (lower, lemmatize, strip, stem)
                    # 1. check if the default nonwords REGEX filter is requested, if so, use it.
                    # 2. check if a customized nonwords REGES filter is provided, if so, use it.
                    # 3. make sure the word isn't in the provided (or empty) set of nonwords
                    if w and (not self.nonwords or not re.match(r'^' + RE_NONWORD + '$', w)) and (
                            not self.nonwords_regex or not self.nonwords_regex.match(w)) and (
                            w not in self.nonwords_set):
                        yield w

    # can these all just be left to default assignments in __init__ or as class methods assigned to global `passthrough()`
    def strip(self, s):
        """Strip punctuation surrounding a token"""
        return s

    def stem(self, s):
        """Find the lexial root of a word, e.g. convert 'running' to 'run'"""
        return s

    def lemmatize(self, s):
        """Find the semantic root of a word, e.g. convert 'was' to 'be'"""
        return s

    def __getstate__(self):
        return self.__dict__

    def __setstate__(self, d):
        self.__dict__.update(d)


def lsi(tokenize=None, iter_dics=None, ram=0.4, num_docs=5000, num_topics=200, num_tokens=1000000,
        num_plots=4, local_path=DATA_PATH, suffix='', ngrams=2,
        verbose=1, show=True, save=True, **kwargs):
    """Train an LSI model on a "corpus" of documnets, like tweets

    Arguments:
      tokenize (callable): Function that returns a sequence of tokens (str) when passed a document (str)
      ram (float):         Portion of RAM to limit the document generator from consuming before StopIteration
      num_docs (int):      Number of documents to limit the document generator to before StopIteration
      num_topics (int):    See gensim.models.LsiModel, default: 200
      chunksize (int):     See gensim.models.LsiModel, default: 10000
      power_iters (int):   See gensim.models.LsiModel, default: None
      extra_samples (int): See gensim.models.LsiModel, default: None

    My process the document generator 3 times (internal tees maintained to "reset" the generator):

    1. "train" Dictionary (Vocab): find set of unique tokens and assigned int IDs)
    2. "train" TfidfModel transform: need global frequencies (by tokenizing docs from document generator) for DF (document freuency) part
    3. "train" LsiModel transform: need to iterate through the word vectors which are generated afresh by retokenizing documents

    TODO: GET RID OF UNUSED ARGS!
          Does the order of documents affect the resulting PCA topics?
          Are topics limited to 10 tokens in gensim?
          Should matches/pairs follow one another?
          Should nonmatching vocab be used at all?

    >>> lsi(ram=0.1, num_docs=2, verbose=0)
    <gensim.models.lsimodel.LsiModel object at ...>
    """
    lsi_kwargs = {'num_topics': num_topics, 'onepass': True}
    lsi_kwargs.update(kwargs)
    if lsi_kwargs.get('onepass', True) and (lsi_kwargs.get('power_iters', None) or lsi_kwargs.get('extra_samples', None)):
        lsi_kwargs['onepass'] = False
    mem0 = psutil.virtual_memory()
    tokenize = tokenize or Tokenizer(ngrams=ngrams)  # , stem='WordNet', lower=True)
    tokenize('Dummy text to get tokenizer to load any data it needs.')
    mem1_tokenizer = psutil.virtual_memory()
    if verbose:
        print('{} tokenizer used {}B'.format(tokenize, friendly(mem1_tokenizer.used - mem0.used)))
    suffix = suffix or 'auto'
    suffix = ('_' * (bool(suffix) and not suffix.startswith('_'))) + suffix
    docgen_orig = (stringify(d) for d in iter_docs)
    docgen_orig, docgen = tee_gen_limit(docgen_orig, limit=num_docs, ram=ram, interval=1000, verbose=verbose)  # 1st generator copy
    mem2_gen = psutil.virtual_memory()
    vocab = Vocab((tokenize(s) for s in docgen), prune_at=num_tokens)
    mem3_vocab = psutil.virtual_memory()
    if verbose:
        print('Built vocabulary of {} unique words and used {}B of RAM. Total RAM used = {}B or {:.3%}'.format(
              friendly(len(vocab)), friendly(mem3_vocab.used - mem2_gen.used), friendly(mem3_vocab.used - mem0.used),
              1. * (mem3_vocab.total - mem3_vocab.available) / mem3_vocab.available))
    if suffix == '_auto':
        suffix = '_' + str(len(vocab)) + '_{}grams'.format(ngrams)
    full_name = 'lsi' + suffix
    if verbose and save:
        print('Will save LsiModel under the name {}'.format(full_name))
    tfidf = TfidfModel(dictionary=vocab)
    mem4_tfidf = psutil.virtual_memory()
    if verbose:
        print('Built tfidf of {} docs and used {}B of RAM. Total RAM used = {}B or {:.4%}'.format(
              friendly(tfidf.num_docs), friendly(mem4_tfidf.used - mem3_vocab.used), friendly(mem4_tfidf.used - mem0.used),
              1. * (mem4_tfidf.total - mem4_tfidf.available) / mem4_tfidf.available))
    docgen_orig, docgen = tee_gen_limit(docgen_orig, limit=num_docs, ram=ram, interval=1000, verbose=verbose)  # 2nd generator copy
    lsi = LsiModel(tfidf[(vocab.doc2bow(tokenize(s)) for s in docgen_orig)], id2word=vocab, **lsi_kwargs)
    mem5_lsi = psutil.virtual_memory()
    if verbose:
        print('Built LSI model: {} docs, {} terms, {} topics. '.format(
            friendly(lsi.docs_processed), friendly(lsi.num_terms), friendly(lsi.num_topics)))
        print('Used {}B of RAM. Total RAM: {}B or {:.4%}'.format(
            friendly(mem5_lsi.used - mem4_tfidf.used), friendly(mem5_lsi.used - mem0.used),
            1. * (mem5_lsi.total - mem5_lsi.available) / mem5_lsi.available))
    # TODO: Consider marshaling the tokenizer and any other user-specified functions
    #   Marshaling stores the bytecode for the tokenizer rather than just its fully-qualified name
    #   This would prevent changes to the tokenizer code from causing previously pickled objects
    #   to behave differently than when they were pickled.
    if save:
        try_preserve(lsi, name=full_name, local_path=local_path, ext='', verbose=verbose)
        # TODO: set lsi.tfidf.vocab=None # already saved in lsi.id2word
        try_preserve(tokenize, name=full_name + '_tokenizer', local_path=local_path, ext='.pickle', verbose=verbose)
    return lsi
