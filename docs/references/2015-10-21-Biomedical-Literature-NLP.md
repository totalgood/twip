---
layout: post
title: Notes from Data User Group Meetup -- Text Mining Meets Neural Nets
---

Here are my notes from the Data User Group and PDX Data Engineering Meetup presentation titled "Text Mining Meets Neural Nets: Mining the Bio-medical Literature", presented by [Dan Sullivan](https://www.linkedin.com/in/dansullivanpdx), the enterprise architect for Cambria Health and Ph.D. student at Virginia Tech (the Biomed Institute).

Dan's thesis involves using machine learning to classify sentences according to relevance to topic of "virulence factor."


# Meaning of Words

All natural language processing starts with words. There are 2 main approaches to assigning meaning to words.

- logical definition of a word like chair
- fuzzy representation of a chair/object (as image recognition does)

## [Generative Models](https://en.wikipedia.org/wiki/Generative_grammar)

Noam Chomsky invented and promoted the idea that words have no inherent meaning and that they merely have statistical rules that determine their sequence and how they will trigger "meaning" or response in a brain that can perceive those word sequences.

- meaning of words is largely of a function of how it relates to other
- 100's of biomed ontologies (graphs of relationships between concepts), very labor intensive

# Topic Modeling

Topic modeling (similar to sentiment analysis)

- LSA Latent semantic analysis
- LDA Latent Dirlich allocaiton distribution of topics across a document, infer topic from data, no training
  - starts with conditional probs
    prob of a topic
    prob of a word associated with a topic

# Classification

Another quinessential topic

- SVM works well (linear model)
- ensembles work OK (random forest)
- KNN works OK

e.g. classifiy as a sentence about virulence factors or not
- requires labeled data to train

# TFIDF

tf(t, d) = num occurrences of t in d
D in all documents (corpus)
idf = log(N / |d in D: t in D|)

tfidf = tf * idf

Note: "one hot" representation only a single count/1 for a single word, each document represented by a single word

# Reducing Dimensions
- ignoring stopwords
- word stemming
- lowercasing

# SVM's

- 90% accuracy on virulence factor classification of sentences
- more data failed to help
- tried about 10 different models and none did much better
- parameter tuning is the last marginal improvement
- feature engineering (expensive, slow, doesn't scale, domain-specific)
- representation (TFIDF) doesn't capture semantic similarity, so got rid of it


# Deep Learning

- word representations
  - word embedding (unstructured)
  - math works
    - plurality direction/distance is additive property
    - sex
    - country-capital relationships
    - part-of
- classification model
  - neural net (structured)
    - enabled by GPUs


# Implementations

Word2Vec
  - CBOW (continuous bag of words) works better if you have common terms used a lot
  - skip-gram (slower)
GloVe
  - based on word cooccurrences (very similar to Word2Vec)

Negation is missed by CBOW (even with bigram and trigrams)
  - antimalaria is about .7 cosine distance from malaria
  - dehydrate and hydrate close to each other by cosine distance

Taxonomic membership is missed
   - A particular/specific Salmonella, called stapholococci wasn't even on the list

It's all about word neighborhood rather than synonomy or semantic similarity.


# Three Neuron Activation Functions

In order of performance for Biomed NLP example:

1. RELU rectilinear gave good performance (linear between thresholds)
2. Hyperbolic tangent (-1 to +1)
3. Sigmoid (0 to 1) worst performance


# Stochastic Gradient Decent

- randomized balls rolling downhill to local minima
- multiple "balls"
- second order gradient decent just converges to local minima faster


# Enhancements to basic NNs

- Convolutional Neural Net
  - Panning window to identify features
- Max pooling operation
  - take maxes
- Recurrent nets applied to language a lot


# Manifold Hypothesis

Entities that cluster around each other in hyperdimensional space that can be much lower dimensional.

Note: Saddle points are common in hyperdimensional space.


# Needs/Ideas/TBD

- Mathematical model of semantics (analogy algebra)
-

# Tools

Theano
Torch
PyLearn2
Lasagne
Keras
DeepDist (works on Spark)
Deeplearnign4J (Java + Scala, Hadoop and Spark)

# References

- [Word2Vec using CBOW, skipgrams, GLoVe](http://arxiv.org/pdf/1301.3781.pdf)
- [SVMs for NLP](http://en.wikipedia.org/wiki/File:Svm_max_sep_hyperplane_with_margin.png)
- [Unsupervised sentiment analysis](http://www.keepcalm-o-matic.co.uk/p/keep-calm-theres-no-training-today/)
    - Latent Semantic Indexing (LSI)
    - Latent Dirichlet allocation (LDA)
- ["Probabilistic Topic Models"](http://yosinski.com/mlss12/MLSS-2012-Blei-Probabilistic-Topic-Models/)
- [Neural Nets for NLP using Gradient Descent](http://u.cs.biu.ac.il/~yogo/nnlp.pdf)
- [Improved (stochastic) Gradient Descent](http://blog.datumbox.com/tuning-the-learning-rate-in-gradient-descent/)
- [Deep Learning Resources](http://memkite.com/deep- learning-bibliography/)
- [Deep Learning Reading List](http://deeplearning.net/reading-list/)
- [extracting semantics](http://www.nltk.org/book_1ed/ch08.html)


