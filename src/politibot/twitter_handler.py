import re
import tweepy
import config_manager
from os import path


class TwitterHandler:
    def __init__(self):
        twitter_config = config_manager.get_config('twitter_config')

        auth = tweepy.OAuthHandler(twitter_config['consumer_key'], twitter_config['consumer_secret'])
        auth.set_access_token(twitter_config['access_token'], twitter_config['access_token_secret'])

        self.twitter_api = tweepy.API(auth)

        self.url_pattern = re.compile(r'https?://t.co/\w+', re.RegexFlag.MULTILINE | re.RegexFlag.UNICODE)
        self.rt_pattern = re.compile(r'^RT', re.RegexFlag.MULTILINE | re.RegexFlag.UNICODE)
        self.twitter_config = twitter_config

    def fetch(self, twitter_user, output_dir):
        screen_name = twitter_user['screen_name']
        user = self.twitter_api.get_user(screen_name=screen_name)
        tweets = self._get_all_tweets(user.id, user.status.id)
        print('{} total tweets: {}'.format(screen_name, len(tweets)))
        tweets_text = [self._clean_tweet(tweet.full_text) for tweet in tweets if self._is_valid(tweet)]
        print('{} total relevant tweets: {}'.format(screen_name, len(tweets_text)))
        with open(path.join(output_dir, screen_name), 'w', encoding='utf8') as f:
            f.write('\n'.join(tweets_text))
        return tweets_text

    def fetch_all(self, output_dir):
        twitter_users = config_manager.get_config('twitter_users')

        for twitter_user in twitter_users:
            self.fetch(twitter_user, output_dir)

    def tweet(self):
        pass

    def _get_all_tweets(self, user_id, last_tweet_id):
        tweets = []
        max_id = last_tweet_id
        try:
            for i in range(self.twitter_config['max_pages']):
                timeline = self.twitter_api.user_timeline(user_id=user_id, max_id=max_id, count=200,
                                                          tweet_mode='extended')
                tweets = tweets + timeline
                if not timeline:
                    break
                max_id = min(timeline, key=lambda t: t.id).id - 1
        except Exception as e:
            print(e)
        finally:
            return tweets

    def _clean_tweet(self, text):
        return self.url_pattern.sub('', text)

    def _is_valid(self, tweet):
        return tweet.in_reply_to_screen_name is None and self.rt_pattern.match(tweet.full_text) is None
