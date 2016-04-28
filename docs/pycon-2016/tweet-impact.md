# Tweet Impact

## Twitter Analytics

Twitter may have more analytics than their sharing through their API, but here some things to think about:

### Engagement Rate?

Replies? Favorites? Mouseover?

### Link Clicks

Obviously want to count this, if you can, but don't forget to normalize for the existence of links (Twitter Analytics doesn't normalize, because they want to encourage link sharing). My "Top Tweets" were only those with links.

### Retweets

Another obvious thing to track, available in the API, which leads us to the concept of "Reach" or "Impressions."

<img src="twitter-analytics-dashboard.png">

### Likes

### Replies

## Reach

An industry standard metric for marketing impact is "reach" which is the people who might have viewed your tweet. It counts the total followers of those that retrweet or fave your tweet. In most cases marketers aren't interested in measuring this accurately, but let's be scientific about it. We actually do care about the impact/reach of our tweets.

The counts should be proprated/weighted by the likelihood that a follower actually read your tweet. You can estimate this by the amount of stuff people actually read from that particular source, or genre or circle of friends. For instance, if the retweeter is favorited/starred by followers, those followers should be given a reach weight of 1.0. If a follower retweets, reacts, or favorites the tweets of their followees 5% of the tweets those folowees send out, then the weight should be something greater than 0.05, perhaps 4x, 0.2, based on statistics about the number of tweets read vs reacted to for that demographic, etc. This is a rabbit hole of machine learning and statistical modeling. We'll just stick with a 0.01 weight for followers and 1.0 for starred followers. Your impact predictor should to better if you want to be more sensitive to your reader.

## Hate Like

Speaking os sensitivity. Did you know that sometimes a like/favorite isn't really a like? Sometimes it's just the opositve.

Is there any way to distinguish Hate-Likes from real Likes? Positive sentiment from bad?  Sentiment analysis on tweet and comments about it and retweet/quotes and general negativity of those that do the liking/forwarding/quoting/commenting. Any way to measure sarcasm? NLP could do a lot of work here to characterize hate-likers by the type of language they use and derate any likes they do appropriately.

