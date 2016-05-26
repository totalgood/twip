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

Additional scripts can be found in ../twip/scripts/ such as

- cat_tweets -- combine tweetget json dump files into single large CSV

Install with pip -e (so you can edit source code and still have a handy CLI in your `$PATH`)

```bash
$ pip install -e /path/to/twip
$ cat_tweets --help
```
