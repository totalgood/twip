---
layout: slides
lang: en
theme: moon
transition: fade  # none/fade/slide/convex/concave/zoom
center: false
revealjs-url: http://lab.hakim.se/reveal-js
# fails because CDNs don't serve up /css etc
# revealjs-url: https://cdnjs.cloudflare.com/ajax/libs/reveal.js/3.3.0/js/reveal.min.js
---

# Making An Impact with Python NLP

---

# Schedule

- 1:20 Introduction
- 1:30 Lesson 1 - Get Tweets
- 1:50 Workshop 1
- 2:10 Lesson 2 - Get Features 
- 2:35 Workshop 2
- 3:00 Refuel (Coffee Break)
- 3:20 Lesson 3 - Unsupervised Learning
- 3:40 Workshop 3
- 4:00 Lesson 4 - Supervised Learning
- 4:20 Workshop 5
- 4:40 Advanced Discussion


# Resources

- [Slides](http://totalgood.github.io/talks/2016-05-29-Making-An-Impact-with-Python-Natural-Language Processing-Tools.html)
- [Twip Repo](https://github.com/totalgood/twip)
- [Set up a VirtualBox](https://github.com/talentpair/puppet-python-nlp-tools)
- Development Environment Alternatives
    - [Install Twip from Source](https://github.com/totalgood/twip/install.md#install)
    - `pip install twip`
    - [Installing a VirtualBox](https://github.com/talentpair/puppet-python-nlp-tools)
    - [IDE and Tool Recommendations for your Laptop](https://github.com/hackoregon/hack-university-machine-learning/blob/master/docs/install.md#install)
    - [An Alternative Data Science Toolbox](http://datasciencetoolbox.org/)

- [Data Science Toolbox](http://datasciencetoolbox.org/)


# Lesson 1

## Get Tweets

### Dan Fellin


# Workshop 1

1. Get Twitter API key
2. Download some tweets
    - your profile
    - a friend's profile
    - a search (see cron.py)
3. Plot some statistics
    - tweets per day
    - favorites per tweet
    - histogram of state for each day of the week

# Lesson 2

## Finding Features in Natural Language

## Finding Features in Tweet Dumps (json, csv)

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

# [MathJax Matrix Example](https://en.wikibooks.org/wiki/LaTeX/Mathematics)

$$A_{m,n} = 
 \begin{pmatrix}
  a_{1,1} & a_{1,2} & \cdots & a_{1,n} \\
  a_{2,1} & a_{2,2} & \cdots & a_{2,n} \\
  \vdots  & \vdots  & \ddots & \vdots  \\
  a_{m,1} & a_{m,2} & \cdots & a_{m,n} 
 \end{pmatrix}$$

# [MathJax Sum and Speaker Note](https://github.com/hakimel/reveal.js/blob/dev/README.md#slide-transitions)

$$\sum_{\substack{
   0<i<m \\
   0<j<n
  }} 
 P(i,j)$$

<aside class="notes">
    Oh hey, these are some notes. They'll be hidden in your presentation, but you can see them if you open the speaker notes window (hit 's' on your keyboard).
</aside>
---


