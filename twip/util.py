"""gensim equivalents for several pciapp.utility and build_training_set functions

TODO:
Architecture is needlessly convoluted, converting from models to querysets to valuesquerysets
to iterators on tokenized strings to sparse 2-D arrays of vectorized documents

>>> bows = BOWGen()
>>> print(list(bows))
[[(0, 1), (1, 1), (2, 1)], [], [(3, 1),...]]
>>> bows.last
[(12, 1), (24, 1), (26, 1), (41, 1), (42, 1)]
>>> bows.last_tokens
['To', 'sail', 'upon', 'the', 'se']
>>> [bows.id2token[i] for i in range(4)]
[u'Sir', u'Spens', u'Patrick', u'king']
>>> bows.token2id['get']
15
>>> from gensim.models import TfidfModel, LsiModel
>>> tfidf = TfidfModel(bows)
>>> print(tfidf)
TfidfModel(num_docs=31, num_nnz=146)

Uncapitalized "the" occurs in the most documents (lines of the "Sir Patrick Spens" poem).
The token "the" appears in 8 lines in the example "corpus" of 31 documents (lines of poetry).
It's vocab/token ID is 12
>>> sorted(zip(tfidf.dfs.values(), tfidf.dfs.keys(), [bows.vocab[i] for i in tfidf.dfs.keys()]), reverse=True)
[(8, 12, u'the'),
 (6, 6, u'The'),
 (5, 55, u'to'),
 (5, 2, u'Patrick'),
 ...
>>> bows.token2id["the"]
12
>>> bows.id2token[12]
u'the'

doc2bow ignores words not in the vocabulary from the 1st read or the document generator
>>> bows.vocab.doc2bow(Tokenizer('Sir Patrick Spens Sir who is this has done this'))
[(0, 2), (1, 1), (2, 1), (22, 2), (38, 1), (45, 1)]

The only word to occur twice in this BOW from a mashup of two "docs" is id #22, "this"
>>> bows.vocab.id2token[22]
u'this'
>>> bows.vocab.doc2bow(Tokenizer().tokenize('Sir Patrick Spens Sir wha is this has done this'))
[(0, 2), (1, 1), (2, 1), (22, 2), (38, 1), (45, 1), (86, 1)]
>>> bows.vocab.id2token[86]
u'wha'

"""
from __future__ import division, print_function, absolute_import
# `pip install future` for universal python2/3
from past.builtins import basestring

import os
from traceback import print_exc
import pickle
import json
import re
from itertools import islice, izip, tee
import logging

from boto.s3.connection import S3ResponseError

from gensim.corpora import TextCorpus, Dictionary

# from django.db.models.query import QuerySet, ValuesQuerySet
from clayton.util import exponential_verbosity, safe_mod
from clayton.s3_util import s3_pull, s3_push, TMP_PATH
from clayton.regex import CRE_TOKEN, RE_NONWORD
from clayton.util import stringify, to_ascii, gen_qs_docs_name, str_strip, str_lower
from clayton.nlp import list_ngrams, make_named_stemmer

log = logging.getLogger('loggly')
passthrough = passthrough  # for flake8 and so nonstemming Tokenizer that uses passthrough can be unpickled


class Tokenizer(object):
    """Callable and iterable class that yields substrings split on spaces or other configurable delimitters.

    For both __init__ and __call__, doc is the first arg.
    TODO: All args and functionality of __init__() and __call__() should be the same.

    FIXME: Implement the `nltk.tokenize.TokenizerI` interface
           Is it at all pythonic to make a class callable and iterable?
           Is it pythonic to have to instantiate a TokenizerI instance and then call that instance's `tokenize` method?

    >>> abc = (chr(ord('a') + (i % 26)) for i in xrange(1000))
    >>> tokenize = Tokenizer(ngrams=5)
    >>> list(tokenize(None))
    []
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
    ["Here're", 'pleasure', u'provide', 'some', 'stemmable', 'your']
    """
    __safe_for_unpickling__ = True

    def __init__(self, doc=None, regex=CRE_TOKEN, strip=True, nonwords=False, nonwords_set=None, nonwords_regex=RE_NONWORD,
                 lower=None, stem=None, ngram_delim=' ', ngrams=1):
        # specific set of characters to strip
        self.ngram_delim = ngram_delim
        self.strip_chars = None
        if isinstance(strip, str):
            self.strip_chars = strip
            # strip_chars takes care of the stripping config, so no need for strip function anymore
            self.strip = None
        elif strip is True:
            self.strip_chars = '-_*`()"' + '"'
        strip = strip or None
        # strip whitespace, overrides strip() method
        self.strip = strip if callable(strip) else (str_strip if strip else None)
        self.doc = stringify(doc)
        self.regex = regex
        if isinstance(self.regex, str):
            self.regex = re.compile(self.regex)
        self.nonwords = nonwords  # whether to use the default REGEX for nonwords
        self.nonwords_set = nonwords_set or set()
        self.nonwords_regex = nonwords_regex
        self.lower = lower if callable(lower) else (str_lower if lower else None)
        self.stemmer_name, self.stem = make_named_stemmer(stem)  # stem can be a callable Stemmer instance or just a function
        self.ngrams = ngrams or 1  # ngram degree, number of ngrams per token
        if isinstance(self.nonwords_regex, str):
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
        self.doc = stringify(doc)
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
        raise NotImplementedError("span_tokenizer and span_tokenzie_sents not yet implemented. ;)")
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
            for i in range(ngrams):
                igrams = [islice(self.__iter__(ngrams=1), j, None) for j in range(i + 1)]
                for tok_tuple in izip(*igrams):
                    yield self.ngram_delim.join(tok_tuple)
        else:
            for w in self.regex.finditer(self.doc):
                if w:
                    w = w.group()
                    w = w if not self.strip_chars else str_strip(w, self.strip_chars)
                    w = w if not self.strip else self.strip(w)
                    w = w if not self.stem else self.stem(w)
                    w = w if not self.lemmatize else self.lemmatize(w)
                    w = w if not self.lower else self.lower(w)

                    # 1. check if the default nonwords REGEX filter is requested, if so, use it.
                    # 2. check if a customized nonwords REGEX filter is provided, if so, use it.
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


def make_tokenizer(tokenizer=Tokenizer, stem=False, strip=None, nonwords=None, lower=None):
    # always return a tokenizer, even if you request a None tokenizer
    if isinstance(tokenizer, str):
        for ext in ('', '_tokenizer.pickle', '_tokenizer', '.pickle'):
            try:
                obj = depreserve(filename=tokenizer.rstrip('._') + ext, ext='', multifile=False)
                log.info("Successfully depreserved {}{} as {}".format(tokenizer, ext, obj))
                return obj
            except (S3ResponseError, IOError):
                log.info('Unable to find file named {}{}'.format(tokenizer, ext))
        log.error('Unable to find a tokenzer by the name {}'.format(repr(tokenizer)))
    tokenizer = tokenizer or Tokenizer
    if isinstance(tokenizer, type) and tokenizer.__name__ == 'Tokenizer':
        tokenizer = tokenizer(stem=stem, strip=strip, nonwords=nonwords, lower=lower)
    elif callable(tokenizer):
        return tokenizer
    return getattr(tokenizer, 'tokenize', tokenizer)


def compile_vocab(docs, limit=1e6, verbose=0, tokenizer=Tokenizer(stem=None, lower=None, strip=None)):
    """Get the set of words used anywhere in a sequence of documents and assign an integer id

    This vectorizer is much faster than the scikit-learn version (and only requires low/constant RAM ?).

    >>> gen = ('label: ' + chr(ord('A') + i % 3)*3 for i in range(11))
    >>> d = compile_vocab(gen, verbose=0)
    >>> d
    <gensim.corpora.dictionary.Dictionary ...>
    >>> print(d)
    Dictionary(4 unique tokens: [u'AAA', u'BBB', u'CCC', u'label'])
    >>> sorted(d.token2id.values())
    [0, 1, 2, 3]
    >>> sorted(d.token2id.keys())
    [u'AAA', u'BBB', u'CCC', u'label']
    """
    tokenizer = make_tokenizer(tokenizer)
    d = Dictionary()

    verbose_factor = exponential_verbosity(verbose)
    try:
        limit = min(limit, docs.count())
        docs = docs.iterator()
    except (AttributeError, TypeError):
        pass
    for i, doc in enumerate(docs):
        # if isinstance(doc, (tuple, list)) and len(doc) == 2 and isinstance(doc[1], int):
        #     doc, score = docs
        try:
            # in case docs is a values() queryset (dicts of records in a DB table)
            doc = doc.values()
        except AttributeError:  # doc already is a values_list
            if not isinstance(doc, str):
                doc = ' '.join([stringify(v) for v in doc])
            else:
                doc = stringify(doc)
        if i >= limit:
            break
        d.add_documents([list(tokenizer(doc))])
        if verbose and (verbose_factor < 1e-3 or not safe_mod(i, int(limit * verbose_factor))):
            log.info('{}: {}'.format(i, repr(d)[:120]))
    return d


def model_dict(docs=None, limit=1e6, verbose=1,
               min_df=2, max_df=1, stop_words=['0', 'null', 'None', 'is', 'are', 'it', 'the', 'a', 'an'],
               **filter_kwargs):
    """Identify all the unique words across a corpus (sequence of documents) and assign an id to each

    Thin wrapper around gs_util.compile_vocab to handle the verbose and limit args and filter a queryset
    of NeoMatch records.

    >>> gen = ('label: ' + chr(ord('A') + i % 3)*3 for i in range(11))
    >>> d = model_dict(gen, verbose=0)
    >>> d
    <gensim.corpora.dictionary.Dictionary ...>
    >>> sorted(d.token2id.values())
    [0, 1, 2, 3]
    >>> sorted(d.token2id.keys())
    [u'AAA', u'BBB', u'CCC', u'label']
    """
    docs = docs or filter_kwargs.pop('qs', None)
    if isinstance(docs, str):
        docs = gen_qs_docs_name(docs, score__gte=0.9, verbose=verbose)

    d = compile_vocab(docs, limit=limit, verbose=verbose, tokenizer=Tokenizer)
    # incorporate this feature reduction into a Vocab class
    stop_ids = [d.token2id[tok] for tok in stop_words
                if tok in d.token2id]
    infrequent_ids = [tokenid for tokenid, df in d.dfs.iteritems() if df < min_df]
    d.filter_tokens(stop_ids + infrequent_ids)  # remove useless words
    d.compactify()                              # remove gaps in id seq
    return d


def gen_bows(docs=None, vocab=None, limit=1e6, verbose=1, tokenizer=Tokenizer):
    """Generate (yield) a sequence of vectorized documents in gensim format

    Gensim calls a set of word vectors (BOWs) a `Corpus`

    Yield:
      Mapping: mapping between word id and word count (a word vector or BOW)
               associated with a single document (text string)
    """
    if vocab is None:
        vocab = compile_vocab(docs=docs, limit=limit, verbose=verbose, tokenizer=Tokenizer)
    for doc in docs:
        yield vocab.doc2bow(tokenizer(doc))


def gen_file_lines(path=EXAMPLE_TEXT_FILE, mode='rUb', strip_eol=True, ascii=True, eol='\n'):
    """Generate a sequence of "documents" from the lines in a file

    Arguments:
      path (file or str): path to a file or an open file_obj ready to be read
      mode (str): file mode to open a file in
      strip_eol (bool): whether to strip the EOL char from lines as they are read/generated/yielded
      ascii (bool): whether to use the stringify and to_ascii functions on each line
      eol (str): UNUSED character delimitting lines in the file

    TODO:
      Use `eol` to split lines (currently ignored because use `file.readline` doesn't have EOL arg)
    """
    if isinstance(path, str):
        path = open(path, mode)
    with path:
        # TODO: read one char at a time looking for the eol char and yielding the interveening chars
        for line in path:
            if ascii:
                line = stringify(line)
            if strip_eol:
                line = line.rstrip('\n')
            yield line


# TODO: eol is unused
# TODO: close file or use it as context within iterator
class FileLineGen(object):

    def __init__(self, path=None, mode='rUb', eol='\n'):
        self.path = path or EXAMPLE_TEXT_FILE
        # open the file so exception raised if does not exist
        if isinstance(self.path, str):
            self.file_obj = open(self.path, mode)
        self.path = self.file_obj.name
        self.eol = eol  # TODO: unused

    def __iter__(self):
        for line in gen_file_lines(path=self.path):
            yield line


# TODO: Unused and should inherit FileLineGen
class FileBOWGen(object):

    def __init__(self, path=None, verbose=0):
        self.verbose = verbose or 0
        self.path = path
        self.vocab = compile_vocab(FileLineGen(path), verbose=self.verbose)
        self.num_lines = None

    def __iter__(self):
        for line in FileLineGen(self.path):
            self.num_lines = (self.num_lines or 0) + 1
            # assume there's one document per line, tokens separated by whitespace
            yield self.vocab.doc2bow(line.lower().split())


def interleave_skip(iterables, limit=None):
    """Like `chain.from_iterable(izip(*iterables))` but doesn't stop at the end of shortest iterable

    TODO: equivalent to chain.from_iterable(izip_longest(*iterables)) if obj is not None)

    >>> tuple(interleave_skip(s for s in ('ABCD', 'vwxyz', '12')))
    ('A', 'v', '1', 'B', 'w', '2', 'C', 'x', 'D', 'y', 'z')
    >>> list(interleave_skip((g for g in [xrange(10), xrange(20,25,1)])))
    [0, 20, 1, 21, 2, 22, 3, 23, 4, 24, 5, 6, 7, 8, 9]
    """

    iterators = map(iter, iterables)
    while iterators:
        for i, it in enumerate(iterators):
            try:
                yield next(it)
            except StopIteration:
                del iterators[i]


class BOWGen(object):
    """Sparse Bag-of-Words, Vocabulary (gensim.Dictionary) and TFIDF generator

    First pass through the documents computes the total vocab counts across all documents
    Second pass computes the normalized TFIDF vector for each doc

    Methods:
      tokenize: user-configurable token segmenter (typically splits a string on spaces)
      vectorize: tokenize a string and count token occurences, return a mapping to counts
      __iter__: iteratively yield a BOW for each document
        BOW = `gensim.doc2bow()` output, a vectorized (real-valued vectors) documents (strings)

    FIXME:
      __init__ should be instantaneous and should not iterate through the queryset

    TODO:
      inherit or imitate `gensim.examples.dmlcorpus.DmlCorpus`
      method to add document to vocab
      implement __len__ method (like gensim.DmlCorpus)
      self.docs is a list of doc IDs (like gensim.DmlCorpus)
    """
    def __init__(self, docs=None, vocab=None, tfidf=None, limit=1e5,
                 tokenizer=Tokenizer, eod='\n', num_docs=None, score=0.9,
                 verbose=0):
        # reset lazy attributes waiting for iteration through docss before being populated
        self.docs = docs
        self.limit = limit
        self.score = score or 0
        self.verbose = verbose
        self._num_docs = min(num_docs, self.limit)  # None if not yet counted
        self.reset(self.docs)

        self.token2id = None

        # record kwarg configuration options
        self._vocab = vocab
        self.id2token = self._vocab
        self._tfidf = tfidf
        self.tokenize = make_tokenizer(tokenizer)
        self.eod = eod  # like EOL or EOF, but "End of Doc" (could be EOL or EOF or another separator)

    def reset(self, docs=None, num_docs=None):
        self.docs = docs or self.docs or EXAMPLE_TEXT_FILE  # TODO: don't default to a test example, just leave None
        self.last = None
        self.last_tokens = None
        self._num_docs = min(self.num_docs, self.limit)  # None if not yet counted
        self.docs_counter = 0
        # make self.docs a property and attempt to count them whenever it is set
        self.scores = [None] * (self.num_docs or 0)
        self.doc_ids = [None] * (self.num_docs or 0)

    def num_docs():
        doc = """__len__ of the `docs` sequence/generator/queryset of strings

                 TODO:
                   * separate self.limitted_num_docs property
                   * don't call num_docs or __len__ property internally unless absolutely necessary
                   * don't update self._num_docs here, but rather within _gen_docs?
                 """

        def fget(self):
            if isinstance(self._num_docs, int) and self._num_docs >= 0:
                if self.verbose > 2:
                    print('Previously counted docs = {}.'.format(self._num_docs))
                return self._num_docs
            # # FIXME: this will never work because querysets are never passed to docs attribute,
            # #        and gen_qs_docs_name() returns a generator not a QuerySet
            # try:
            #     self._num_docs = min(self.docs.count(), self.limit)
            # except:
            #     pass
            # if not isinstance(self.docs, str):
            #     try:
            #         self._num_docs = min(len(self.docs), self.limit)
            #     except:
            #         pass
            else:
                # TODO: check len(self.tfidf) too, before iterating through gen, it may have already been provided during init!
                count = 0
                for d in self._gen_docs():
                    if count >= self.limit:
                        break
                    count += 1
                self._num_docs = count
                if self.verbose:
                    print('Counted up docs in generator and found {}.'.format(self._num_docs))

            if self.verbose > 1:
                print('Got len or count of docs and found {}.'.format(self._num_docs))
            return self._num_docs
        return locals()
    num_docs = property(**num_docs())

    def verbose():
        doc = "Verbosity (frequency of progress `print`s (3 = debug, 1 = normal, 0 = quiet)"

        def fget(self):
            return getattr(self, '_verbose', None)

        def fset(self, value):
            self._verbose_factor = exponential_verbosity(value)
            self._verbose = value

        def fdel(self):
            del self._verbose

        return locals()
    verbose = property(**verbose())

    @property
    def vocab(self):
        if self._vocab is None:
            # TODO: DRY this up by calling the setter
            self._vocab = compile_vocab(docs=self._gen_docs(), limit=self.limit, verbose=self.verbose,
                                        tokenizer=self.tokenize)
            self.token2id = self._vocab.token2id
            self.id2token = self._vocab
        return self._vocab

    @vocab.setter
    def vocab(self, value):
        if isinstance(value, Vocab):
            self._vocab = value
        else:
            self.docs = value
            self._vocab = compile_vocab(docs=self._gen_docs(), limit=self.limit, verbose=self.verbose,
                                        tokenizer=self.tokenize)
        self.id2token = self._vocab

    @property
    def tfidf(self):
        if not self._tfidf:
            self._tfidf = TfidfModel(self)
        return self._tfidf

    @tfidf.setter
    def tfidf(self, value):
        if isinstance(value, TfidfModel):
            self._tfidf = value
        else:
            self.docs = value
            self.vocab = self.docs  # calls the vocab setter/compiler
            self._tfidf = TfidfModel(self)

    def _gen_tfidf_scores(self):
        """Yield (doc_tfidf, score) 2-tuple for each doc in self.docs"""
        # # FIXME: self.reset() should be called within a self.docs property which should also set a self._iterable_docs attribute
        # self.reset()
        return zip(self.tfidf, self.scores)

    def _gen_docs_scores(self):
        """Yield (doc, score) 2-tuple for each doc in self.docs, stopping at self.limit and obeying self.verbose

        FIXME: align scores with doc_ids and doc_gen:
            >> both.doc_ids[0]
            0
            >> both.doc_ids[-1]
            19999
            >> len(both.doc_ids)
            20000
            >> print(both.scores[0])
            None
            >> len(both.scores)
            20001
            >> both.num_docs
            20000
        """
        # # FIXME: self.reset() should be called within a self.docs property which should also set a self._iterable_docs attribute
        # self.reset()
        # TODO: only these vars should be reset in self.reset?
        self.docs_counter = 0  # number of docs that have been scored and have an entry in the self.scores list
        self.scores = [None] * (self.num_docs or 0)
        self.doc_ids = [None] * (self.num_docs or 0)
        for i, doc in enumerate(self._gen_docs(with_score=True)):
            # if i > self.num_docs:
            #     break
            try:
                doc = doc['text'], doc['score']
            except (KeyError, TypeError):
                pass
            if len(doc) == 2 and isinstance(doc[1], (int, float)):
                self.docs_counter += 1
                if 0 < len(self.doc_ids) <= i:
                    self.doc_ids += [i]
                else:
                    self.doc_ids = [i]
                if self.docs_counter > len(self.scores):
                    self.scores += [doc[1]]
                else:
                    # overwrite previous score for last pass through? TODO: check for None score first
                    self.scores[self.docs_counter - 1] = doc[1]
                yield doc[0]

    def _gen_docs(self, docs=None, with_score=False, verbose=None):
        """Generate a sequence of documents (strings) from the provided docs name, path, or queryset"""
        self.docs = docs or self.docs
        if isinstance(self.docs, str):
            try:
                if with_score:
                    return ((doc, 0) for doc in FileLineGen(self.docs))
                else:
                    return FileLineGen(self.docs)
            except:
                try:
                    qs_gen = gen_qs_docs_name(self.docs, with_score=with_score, limit=self.limit, score__gte=self.score, verbose=verbose)
                    if verbose > 2:
                        print 'Used pciapp.utility.gen_qs_docs_scores_name("{}") to retrieve "documents" (strings) from database in qs={}.'.format(
                            self.docs, qs_gen)
                    return qs_gen
                except ValueError:
                    if verbose > 2:
                        print_exc()
                    if with_score:
                        return ((doc, 0) for (i, doc) in enumerate(self.docs.split(self.eod)) if i < self.limit)
                    else:
                        return (doc for (i, doc) in enumerate(self.docs.split(self.eod)) if i < self.limit)
        if verbose:
            print("Nonstr (type: {}) docs offered up to BOWGen, so iterating through them to generate what's there".format(type(self.docs)))
        return (stringify(doc) if not with_score else (stringify(doc), 0) for (i, doc) in enumerate(self.docs) if i < self.limit)

    def __iter__(self):
        # recreate a new iterator based on the previously set "docs" property (which could be a generator)
        for i, doc in enumerate(self._gen_docs_scores()):
            if self.verbose and (self._verbose_factor < 1e-3 or
                                 (self._verbose_factor and not safe_mod(i, int(len(self) * self._verbose_factor)))):
                print('    {:6d}/{:6d}: {}...'.format(i, self.num_docs, str(doc)[:100 * self.verbose]))
            self.last_tokens = list(self.tokenize(doc))
            if self.verbose > 2 and (self._verbose_factor < 1e-3 or
                                     (self._verbose_factor and not safe_mod(i, int(len(self) * self._verbose_factor)))):
                print('      tokens: {}'.format(self.last_tokens))
            # INFO: The first time self.vocab is accessed an indexer will iterate through all the docs!
            self.last = self.vocab.doc2bow(self.last_tokens)
            if self.verbose and (self._verbose_factor < 1e-3 or
                                 (self._verbose_factor and not safe_mod(i, int(len(self) * self._verbose_factor)))):
                print('BOW {:6d}/{:6d}: {}'.format(i, self.num_docs, str(self.last)[:100 * self.verbose]))
            yield self.last

    def __len__(self):
        return min(self._num_docs or 0, self.limit)

    def vectorize(self, s):
        """Tokenize (segment) a string and count occurences of each word id

        TODO: check for tokens (words) not already in the vocab and add them to it as necessary
              (like vowpel-wabbit, build both the vocab and the word vectors on the fly)
        """
        return self.vocab.doc2bow(self.tokenize(s))

    def __repr__(self):
        return "%s(%r)" % (self.__class__, self.__dict__)


class Matcher(BOWGen):

    def __init__(self, docs=None, vocab=None, limit=1e6, verbose=0, tokenizer=Tokenizer, num_dim=10, eod='\n'):
        super(self, Matcher).__init__(docs=docs, vocab=vocab, limit=limit, verbose=verbose, tokenizer=tokenizer, eod=eod)
        self.num_dim = num_dim
        # # this should iterate through all the docs and compute the tfidf
        # self.tfidf = TfidfModel(self)
        # this should iterate through all the BOWs in the BOWGen and index them
        self.lsi or LsiModel(self, num_topics=num_dim)

    def project(self, doc):
        self.lsi = self.lsi or LsiModel(self, num_topics=self.num_dim)
        self.last = doc or ''
        if isinstance(self.last, str):
            self.last = self.vectorize(doc)
        self.last_tfidf = self.tfidf[doc]
        return self.lsi[self.last_tfidf]

    def add_document(self, doc):
        self.lsi = self.lsi or LsiModel(self, num_topics=self.num_dim)
        self.last = doc or ''
        if isinstance(self.last, str):
            self.last = self.vectorize(doc)
        self.last_tfidf = self.tfidf[doc]
        return self.lsi[self.last_tfidf]
