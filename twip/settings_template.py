# 1. copy this file to settings_secret.py
# 2. make sure the settings_secret.py file is ignored (should be listed in .gitignore)
# 3. EITHER...
#   a) add your TWITTER secrets directly to this file in the `except:` block below
#    **OR**
#   b) set your environment variables to contain your keys (see below for env var names)
# 4. `twyth = Twython(settings_secret.TWITTER_API_KEY, settings_secret.TWITTER_API_SECRET)`

# TWITTER_API_KEY and _SECRET are required to download tweets
try:
    TWITTER_API_KEY = os.getenv('TWITTER_API_KEY')
    TWITTER_API_SECRET = os.getenv('TWITTER_API_SECRET')
except:
    TWITTER_API_KEY = '25AlphaNumericCharactersX'
    TWITTER_API_SECRET = '50AlphaNumericCharactersX50AlphaNumericCharactersX'

# Optional account identifying information that doesn't need to be protected
TWITTER_API_OWNER = 'hobsonlane'  # the app owner's @username
TWITTER_API_OWNER_ID = 59275999   # see the app

# This is how to use these keys to instantiate a Twython connection to the twitter API
# twyth = Twython(TWITTER_API_KEY, TWITTER_API_SECRET)
