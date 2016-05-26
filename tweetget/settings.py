import os

# to get your own keys:
# 1. go to https://apps.twitter.com/
# 2. fill out form and hit create
# 3. go to app and click "manage keys and access tokens"
# 4. copy into your bashrc

TWITTER_API_KEY = os.environ['TWITTER_API_KEY']
TWITTER_API_SECRET = os.environ['TWITTER_API_SECRET']

RATE_LIMIT = 100  # requests every 15 minutes, max is 450 for app twitter api
RATE_LIMIT_WINDOW = 900  # 15 minutes * 60

DATA_DIR = './data/'
OLDEST_ID_PATH = '{}oldest_id.txt'.format(DATA_DIR)
