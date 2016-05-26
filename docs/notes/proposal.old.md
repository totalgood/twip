# Making an Impact with Python Natural Language Processing Tools

## Description

Do your tweets get lost in the shuffle? Would you like to predict a tweet's impact before you hit send? Python now has all the tools to make this possible. Several Python packages for machine learning and natural language processing have reached "critical mass" and can now be combined to perform these and other powerful natural language processing tasks. This tutorial will teach you how.

## Audience

Amateur and professional data scientists who want to learn about a powerful combination of python tools and techniques for natural language processing

## Objectives

Attendees will build a python module that can determine the best time of day to tweet on a particular subject. While building this tool, attendees will become familiar with the most powerful combination of python packages for performing state-of-the-art natural language processing.

## Detailed Abstract

### Prerequisites

Students that have written python scripts, modules, or a package and are familiar with the basic string manipulation and formatting capabilities built into python will have the necessary skill to complete this tutorial. In addition, any students who are familiar with linear algebra, and basic statistics concepts (like probability and variance) will be able to grasp the mathematics behind the tools assembled during the tutorial, but this is not required.

Also, familiarity with scikit.learn and pandas would be helpful, but not necessary.

### Python Development Environment

Students will need iPython, NLTK, scipy, scikit-learn, and Pandas installed on their laptops to run the examples in this tutorial and build the tweet impact predictor tool. Students can use pip to install the [requirements listed here](/requirements.txt). In addition students will need to install the python twitter api or download a 50 MB compressed file of tweets in order to train and test their tweet predictor.

### Overview

Participants will develop a natural language processing pipeline for tweets in three modules. 

The first section of the pipeline will be a natural language feature extractor and normalizer based on python builtin modules `collections`, `string`, and `re`. The Pandas `DataFrame` data structure will also be introduced.

The second section will utilize `scikit-learn` and `numpy` to simplify the feature set to a manageable number of features. It will find optimal combinations of reduced numbers of features that provide the greatest information about the subject matter of the tweets being processed. 

The final section of the pipeline will assemble a training set based on tweet statistics not contained in the natural language content of the tweets and combining this with the natural language features to cluster and classify tweets according to their popularity (number of favorites), and reach (number of potential viewers due to retweets). A neural net will be trained to predict tweet impact (popularity and reach) based on the time of day and day of week as well as the tweet text planned to be sent.

## Outline

### Introduction (10 min)

- Interesting NLP applications
    - chatbots
    - behavior modification
    - natural language generation
- state of the art NLP capabilities
    - skip-grams and Word-Vector math
        - teaser: "king" - "man" + "woman" = "queen"
    - Google Now & Siri
        - description of pipeline (we will build some elements here)

### Feature Extraction with Python (30 min)

- `str.split` to quickly extract words from a tweet
- `collections.Counter` to count word occurrences
- Explore regular expressions in a text adventure
    - Text Adventure games vs. Choose Your Own Adventure books
    - Python Regular Expressions vs. Memoryless Regular Expressions 
    - `re.split` to more accurately extract words (tokens)
    - `nltk` stemmers
    - `nltk` part-of-speech tagging
    - `nltk` word root parsers
    - `nltk` stop word filters
- `pandas.Series` and `pandas.DataFrame`
    - analogy to builtin `collections.OrderedDict`
    - use for storing word vectors
- `np.linalg.norm` and `np.dot` to efficiently normalize word counts and frequencies
- `sklearn...TfidfVectorizer` to efficiently store (sparse) normalized word frequencies
- `np.linalg.norm`, `np.dot` to compute "distances" between tweets
- `sklearn.cluster` to group similar tweets 

### Workshop: Feature Extraction Pipeline (20 min)

Students will use the tools provided in the presentation to build a python function capable of processing 10's of thousands of tweets in a few minutes to produce meaningful clusters based on tweet content.

### Feature Reduction (40 min)

- Feature Reduction
    - Calculating entropy (information value) with `numpy`
    - `sklearn..PCA` Principle Component Analysis
        - how it works (overview of matrix algebra)
        - where it works best
        - what to watch out for
        - apply to tweet TFIDF to reduce vocabulary
- Plotting and Exploring
    - scipy scatter matrix plots
        - visulizing natural language feature vectors
        - projecting/slicing
    - `json.dumps` of TFIDF matrices for d3.js matrix visualizations
    - using python to manipulate nested dicts to create json required for interactive d3.js force-directed graphs 

### Workshop: Feature Reduction (20 min)

Attendees will use the tools provided simplify the natural language feature set extracted from their twitter feeds. They will use scikit-learn to identify more informative clusters and patterns than was possible in the previous workshop.

### Supervised Learning (40 min)

- Extracting numerical statistics about tweets
    - `pandas.DataFrame` `.group_by` and `.hist`
        - time-of-day, day-of-week, day-of-quarter, day-of-year, month-of year
    - Following the trail of retweets
        - Model after Python builtin `os.walk`
    - Favorites/Likes
        - `numpy.corrcoeff` and `numpy.cov` to correlate 
            - numerical metrics
            - tweet subject
            - twitter ID
        - Identify influential "likers"
- Modeling
    - Use builtin `random.sample` to compose test and training data sets
    - `np.linalg.norm` and `np.dot` to calculate tweet similarity
        - `sklearn.cluster.KMeans` to classify tweets by topic
        - `numpy.linalg.norm` similarity to cluster means to score tweets
        - label tweets using `pandas.DataFrame.get` ([]) sql-like queries to threshold score
    - `sklearn..Lasso` for efficient linear regression
     (p-norm, cosine-distance, supremum distance)
- Measuring Model Performance
    - ConfusionMatrix
        - sensitivity
        - specificity
- `sklearn.lda` Linear Discriminant Analysis (use topic labels above)
    - show why model performance is improved relative to PCA alone

### Workshop: Supervised Learning (20 min)

Attendees will mine the Twitter API and data sets provided to compute the numerical statistics and assign scores to each tweet. Attendees will build a `ConfusionMatrix` class that inherits `pandas.DataFrame` and adds a `from_labels` method to injest scored/labeled data. Attendees will also add `accuracy` and `specificity` methods to their class and combine them to create a custom performance metric that targets their individual performance goals for their tweet predictor. They will balance the likelihood of a great tweet and the likelihood of a dud tweet. Attendees will use `sklearn.lda` to reduce dimensions further and generalize the model. Finally attendees will compare their model performance metric with and without the LDA pipeline element to confirm improved performance.

### Advanced NLP (20 min)

- Adding another dimension: word order
    - Intro to scale space processing as alternative to bag-of-words
    - `pandas.DataFrame.rolling_window` to perform 1-D convolution
    - `matplotlib.pyplot.pcolor` + `pandas.DataFrame` = heatmap of twitter streams
- Neural Networks
    - `pybrain2` convolutional neural network to classify tweets
- Word Vectors
    - Skip-grams
    - Utilizing Google's Word2Vec
    - example Word Vector "math"

We will also talk about where to go from here, further advanced techniques and resources for students to explore on their own.

### Workshop: Level Up Your Tweet Predictor (10 min)

Attendees will add scale-space processing to their tweet predictor and plot a topic heatmap of their twitter stream.


## More Info

All material will be accompanied by iPython notebooks and provided in open-source (MIT-licensed) GitHub repositories. Data sets will be prepossessed and compressed to simplify participant environment setup. A sequence of git tags and branches  will provide an "answer key" for workshop activities, to allow students to continue moving forward.

## Notes

Hobson Lane has spoken about natural language processing on 5 previous occasions and have a track record of teaching novices to use natural language processing techniques in a short amount of time. Hobson served for years as a mentor for Georgia Institute of Technology grad students in Machine Learning and am currently mentoring [SlideRule](mysliderule.com) students. Hobson has an engaging presentation style and invokes insightful dialog to promote critical thinking.

## Speaker Bio

Hobson has nearly two decades of engineering and teaching experience in robotics, autonomous systems, data science, and natural language processing. Hobson has relied on Python as his language of choice for Data Science and Natural Language Processing for companies like Squishy Media, Building Energy, Sharp Labs, [Total Good](http://totalgood.com), [Hack Oregon](http://hackoregon.org), Pellego, Intel Labs, and [Talentpair](http://talentpair.com), as well as numerous open source projects.

- Professional profile on [Linked-In](https://www.linkedin.com/in/hobsonlane)
- [GitHub profile](http://github.com/hobson/) with some open source contributions
- Recent talks at [hobsonlane.com/talks](http://hobsonlane.com/talks)