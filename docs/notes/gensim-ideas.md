# Gensim Sprint

- `Dictionary.filter_extremes(no_below=no_below, no_above=no_above, keep_n=keep_n)`
    - use decision tree or entropy measure to select vocabulary rather than cutoff
- `save()` method on model and inconsistent use of `smart_open` which often fails
- `LinearDiscriminantAnalysisModel`
- `QuadraticDiscriminantAnalysisModel`
- a `chainer` or nolearn/Theano neural net Model?
- RAM (Memory)
  - efficient file swapping/caching of dictionary and model sparse matrices?
  - warnings and optional automatic culling as RAM limit approaches
  - incremental model dumps to disk in case of memory overflow
- intrleaving django querysets or other iterators
  - more Corpus classes

