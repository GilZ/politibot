import json
import re

import tweepy
import os.path as path


class TwitterHandler:
    def __init__(self):
        with open(path.join('..', '..', 'config', 'twitter_config.json')) as f:
            twitter_config = json.load(f)

        auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
        auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])

        self.twitter_api = tweepy.API(auth)

        self.url_pattern = re.compile(r'https?://t.co/\w+', re.RegexFlag.MULTILINE | re.RegexFlag.UNICODE)
        self.rt_pattern = re.compile(r'^RT', re.RegexFlag.MULTILINE | re.RegexFlag.UNICODE)
        self.twitter_config = twitter_config

    def fetch(self, twitter_user, output_dir):
        user = self.twitter_api.get_user(screen_name=twitter_user['screen_name'])
        tweets = self._get_all_tweets(user.id, user.status.id)
        print(twitter_user['screen_name'] + ': ' + str(len(tweets)))
        tweets_text = [self._clean_tweet(tweet.text) for tweet in tweets if self._is_valid(tweet)]
        print(twitter_user['screen_name'] + ' filtered: ' + str(len(tweets_text)))
        with open(path.join(output_dir, twitter_user['screen_name']), 'w', encoding='utf8') as f:
            f.write('\n'.join(tweets_text))
        return tweets_text

    def fetch_all(self, output_dir):
        with open("../../config/twitter_users.json") as f:
            twitter_users = json.load(f)

        for twitter_user in twitter_users:
            self.fetch(twitter_user, output_dir)

    def tweet(self):
        pass

    def _get_all_tweets(self, user_id, last_tweet_id):
        tweets = []
        max_id = last_tweet_id
        try:
            for i in range(self.twitter_config['max_pages']):
                timeline = self.twitter_api.user_timeline(user_id=user_id, max_id=max_id, count=200)
                tweets = tweets + timeline
                if not timeline:
                    break
                max_id = min(timeline, key=lambda t: t.id).id - 1
        except Exception as e:
            print(e)
        finally:
            return tweets

    def _clean_tweet(self, text):
        return self.url_pattern.sub('', text).replace('...', '').replace('…', '')

    def _is_valid(self, tweet):
        return tweet.in_reply_to_screen_name is None and self.rt_pattern.match(tweet.text) is None
