---
layout: slides
lang: en
theme: moon
transition: fade  # none/fade/slide/convex/concave/zoom
center: false
revealjs-url: http://lab.hakim.se/reveal-js
# fails because CDNs don't serve up /css etc
# revealjs-url: https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.3.0/js/reveal.min.js
# build with `./build`
# serve the HTML at http://localhost:8000/ with `python -m SimpleHTTPServer`
---

# Lesson 2


# Got Features?


# Features in Tweet Dumps

`tweets.json`

- favorites
- userid, id number
- city, state
- lat, lon
- user settings (geo on, protected account)
- tweet info (promoted, urls)


# Tokens

What's a token?


# Meaning

Smallest meaning bit?

- Statement? Paragraph?
- Sentence?
- Phrase?
- Noun phrase ("python language")
- Word?
- Character?
- Punctuation


# Depends on Your Language

<img src="../images/220px-RNA-codons.png">

If you're RNA you tokens are 

"A", "G", "C", "U"

For DNA it's 

"A", "G", "C", "T"


# If You're a Computer

0's and 1's

<code>
00101010 00000100 0000010 00101010
</code>

Bit, Byte or Word
Which is the Token?


<aside class="notes">
Imagine you wanted to decypher this
Code breakers use frequency analysis
Find most frequent words/letters
Known frequencies for words/letters
Depends on language, context
</aside>

# Computer Language

<code>
OR DL,00101000b
XOR DL,00000010b
HCF
</code>

- Line, statement
- word, symbol

<aside class="notes">
Humans have fun with language
Even Machine Code
Can't help but intepret
</aside>


# Python

`ans = [c for c in "Hello"]`

```.py
    ans = [c for c in "Hello"]
```


# English Words

We'll mangle common multi-word tokens:

- United States -> "States", "United"
- Manchester United -> "Manchester", "United"


# Word2Vect Vectors

Each word is...

- bag of words
- defined by its neighbors 
- all words every used with it

<aside class="notes">
What about dictionary definition?
</aside>


# Word Vectors

Each word is...

- dictionary definition(s)?


# Words

## Wh

# Workshop 2

1. Tokenize Your Tweets
    - case normalization
    - ignore URLs and punctuation
    - transcode smilies?
2. Compile a Vocabulary
    - Count word frequencies
    - Plot a Zipf plot of word frequencies
    - Plot a Zipf plot of document frequencies
3. Compute the TFIDF
    - Term frequency in each tweet
    - Document frequency (which tweets contain the term)


# [Got Features?](2 - Got Features.html)