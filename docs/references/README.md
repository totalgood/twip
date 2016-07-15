# Making Connections with Natural Language Processing

## Description

Have you ever felt like your tweets were falling on deaf ears? Have you wished you could predict how well your tweets would do before you hit send and adjust the timing and content of your tweets to improve them? Now you can! Several Python packages for machine learning and natural language processing have reached "critical mass" and can now be combined to perform these and other powerful natural language processing tasks. This tutorial will teach you how.

## Audience

Amateur and professional data scientists who want to become familiar with the state-of-the-art natural language processing tools that python has to offer.

## Objectives

Attendees will build a python module that can determine the best time of day to tweet on a particular subject. While building this tool, attendees will become familiar with the most powerful combination of python packages for performing state-of-the-art natural language processing.

## Detailed Abstract

Participants will develop a natural language processing pipeline in three modules. The first section of the pipeline will be a natural language feature extractor and normalizer based on python builtins `collections`, `string`, and `re` combined with the powerful Pandas DataFrame data structure. The second section will be a module utilizing scikit-learn and `numpy` to simplify the feature set to a manageable number of features. It will find optimal combinations of reduced numbers of features that provide the greatest information about the subject matter of the tweets being processed. The final section of the pipeline will assemble a training set based on tweet statistics not contained in the natural language content of the tweets and combining this with the natural language features to cluster and classify tweets according to their popularity (number of favorites), and reach (number of potential viewers due to retweets). A neural net will be trained to predict tweet impact (popularity and reach) based on the time of day and day of week as well as the tweet text planned to be sent.

## Outline

