from twitter_handler import TwitterHandler
from tweet_maker import TweetMaker
from os import path, listdir
import json

with open(path.join('..', '..', 'config', 'general.json')) as f:
    original_tweets_dir = json.load(f)['original_tweets_dir']

x = TwitterHandler()
x.fetch_all(original_tweets_dir)

for filename in listdir(original_tweets_dir):
    with open(path.join(original_tweets_dir, filename), encoding='utf8') as f:
        tweets = f.read()
        for i in range(10):
            tweet = TweetMaker.make_tweet(tweets)
            if not tweet:
                continue
            print(filename + ': ' + tweet)  # TODO: post tweet
