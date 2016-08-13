import os

# to get your own keys:
# 1. go to https://apps.twitter.com/
# 2. fill out form and hit create
# 3. go to app and click "manage keys and access tokens"
# 4. copy into your bashrc

TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET = os.environ['TWITTER_API_SECRET']

# Twitter Docs: "Search is rate limited at 180 queries per 15 minute window."
# Twitter enforces rate limits for each window of 15 minutes
RATE_LIMIT_WINDOW = 900  # 15 min * 60 sec / min 
TWEETS_PER_REQUEST = 100

DATA_PATH = './data'

QUERIES = ['python -monty', '#sarcasm', '#happy', '#sad']
