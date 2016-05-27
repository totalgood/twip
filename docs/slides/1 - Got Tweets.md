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


# Lesson 1


# Got Tweets?

**by Dan Fellin**


# Twitter API

- Have you used Twitter API?

- in the last six months?


# Twitter API has all you need for TWIP

Source data is tweets about python.

Let's code!


# What do you think?

That's all there is to it to gather the 200K tweets.

That 200K was twitter's fault. 4x all the tweets for the past week

Any questions?


# Pandas

How many people have used pandas?


# Pandas is...

- fast, flexible data structures (tables)
- efficient for relational (indexed) data
- like `dict` tuned up


# Two core parts:

* Data series: array, row in a table or spreadsheet
* Data frame: array of arrays, table or spreadsheet

Now let's go to code...

# normalize_json

```python
df = get_df_few()  # normalize_json

df.to_csv('out.csv')
# look at csv
# look at json
# explain why normalize_json is cool

# list all columns
df.columns
```

# Dataframe Magic

```python
# all columns are tab completed
# df.fav<TAB>

# append
df2 = get_df_many()  # normalize_json
df_all = df.append(df2)

# favorites
print(df.favorite_count.mean())
print(df.sort_values('favorite_count'))
```


# Unique Words

```python
# get all
print(df.groupby("favorite_count").size())

df_all.created_at_ts = pd.to_datetime(df_all.created_at)

df_all.text_split = df.text.str.lower().str.split()

unique_words = set()
df_all.text_split.apply(unique_words.update)
len(unique_words)  # should be ~20000
```


# Common Words

```python
all_words = []
df_all.text_split.apply(all_words.extend)
len(all_words)  # should be ~140000
c = Counter(all_words)
c.most_common(20)
```

# Important Common Words

```python
# replace all not word and not whitespace
# ALSO LOWER
s = df_all.text.str.replace('[^\w\s]', ' ')
s = s.str.split()
df_all.text_split = s
all_words = []
df_all.text_split.apply(all_words.extend)

c = Counter(all_words)
c.most_common(20)
```


# Workshop 1

Now, choose your own adventure:

1. Pandas: play with tweets (`all_tweets.csv`)
2. Tweetget: nab a Twitter API key some tweets that interest you.
    - your profile
    - a friend's profile
    - a search (see cron.py)


# Extra Credit

3. Plot some statistics
    - tweets per day
    - favorites per tweet
    - histogram of state for each day of the week
