# tweetget

gets all the tweets matching `python -monty` from Twitter and stores
them in a single json file

## api

```bash
# to issue a single request for 100 tweets (max allowed by twitter) and save it as json
python -m tweetget.single

# to request max tweets RATE_LIMIT times
python -m tweetget.core

# to hit Twitter's API every 15 minutes, run this in screen/tmux
python -m tweetget.cron
```
