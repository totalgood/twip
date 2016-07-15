# Dependency Tree

+ twip
  + util
    + find_files
    - dict2obj 
  - 
  - regex
    - CRE_TOKEN
    - RE_NONWORD
    - RE_NONWORD
    - CRE_TOKEN
    - CRE_BAD_FILENAME
    - CRE_WHITESPACE

## critical modules/methods

pug.nlp.stats.Confusion
pug.nlp.constant
pug.nlp.regex.url


## pug.nlp modulef imports

+ stats
- regex
- util
- segmentation
- scrape (only transcode_unicode and only in clean.py)

## grep

```bash
$ grep -r pug twip --include=*.py

twip/util.py:from pug.nlp.regex import CRE_TOKEN, RE_NONWORD
twip/nlp.py:from pug.nlp.regex import RE_NONWORD, CRE_TOKEN, CRE_BAD_FILENAME, CRE_WHITESPACE
twip/train.py:from pug.nlp.regex import RE_TOKEN, RE_NONWORD

twip/scripts/cat_tweets.py:from pug.nlp.util import find_files
twip/scripts/explore.py:from pug.nlp.util import dict2obj
twip/scripts/clean.py:from pug.nlp.util import make_name
twip/constant.py:from pug.nlp.util import mkdir_p
twip/nlp.py:from pug.nlp.util import PrettyDict
twip/wip/build_pycon_slides.py:from pug.nlp.util import mkdir_p

twip/nlp.py:from pug.nlp.segmentation import stringify, passthrough
twip/util.py:from pug.nlp.segmentation import str_strip, str_lower, passthrough
twip/scripts/generate.py:from pug.nlp.segmentation import Tokenizer

twip/scripts/clean.py:from pug.nlp.scrape import transcode_unicode
```

```bash
$ grep -r pug docs --include=*.py

docs/notebooks/99 WIP -- Data Exploration.py:from pug.nlp.util import dict2obj
docs/notebooks/04 Data -- Natural Language.py:from pug.nlp.util import dict2obj
docs/notebooks/21 gensim -- Quanitfied Self.py:from pug.nlp import util
docs/notebooks/11 Learning -- Regression.py:from pug.nlp.stats import Confusion
docs/notebooks/10 Learning -- Predicting Impact.py:from pug.nlp.stats import Confusion
docs/notebooks/03 Data -- Getting Selective.py:from pug.nlp import constant
docs/notebooks/07 Features -- Text.py:from pug.nlp.regex import url
docs/notebooks/02 Data -- Exploration.py:from pug.nlp.util import dict2obj
```

## sublime search

```bash
/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/constant.py:
   11: from pug.nlp.util import mkdir_p

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/nlp.py:
   17: from pug.nlp.regex import RE_NONWORD, CRE_TOKEN, CRE_BAD_FILENAME, CRE_WHITESPACE
   18: from pug.nlp.util import PrettyDict
   19: from pug.nlp.segmentation import stringify, passthrough

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/train.py:
    9: from pug.nlp.regex import RE_TOKEN, RE_NONWORD

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/util.py:
   62: from pug.nlp.regex import CRE_TOKEN, RE_NONWORD
   63: from pug.nlp.segmentation import str_strip, str_lower, passthrough

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/scripts/cat_tweets.py:
   25: from pug.nlp.util import find_files

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/scripts/clean.py:
   92: from pug.nlp.util import make_name
   93: from pug.nlp.scrape import transcode_unicode

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/scripts/explore.py:
   24: from pug.nlp.util import dict2obj

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/scripts/generate.py:
   22: from pug.nlp.segmentation import Tokenizer
   23: # from pug.nlp.constant import MAX_UINT16

/home/hobs/src/twip/build/lib.linux-x86_64-2.7/twip/wip/build_pycon_slides.py:
   14: from pug.nlp.util import mkdir_p
```

