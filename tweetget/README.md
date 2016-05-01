# tweetget

gets all the tweets matching `python -monty` from Twitter and stores
them in a single json file

```bash
cd tweetget

# to run one iteration
python core.py

# to merge all the raw data into data.json
python merge.py

# to run reports on data.json
python report.py

# to read 10 random tweets
python read.py

# to hit Twitter's API every 15 minutes, run this in screen/tmux
python cron.py
```
