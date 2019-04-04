from twitter_handler import TwitterHandler
from tweet_maker import TweetMaker
import config_manager
from os import path, listdir
import argparse


def run():
    parser = argparse.ArgumentParser(description='Generate Israeli politicians\' tweets')
    parser.add_argument('-f', '--fetch', action='store_true', help='Fetch original tweets (default: False)')
    parser.add_argument('-p', '--post', action='store_true', help='Post new tweets (default: False)')

    args = parser.parse_args()

    config = config_manager.get_config('general')
    original_tweets_dir = config['original_tweets_dir']
    new_tweets_file = config['new_tweets_file']

    if args.fetch:
        tweeter_handler = TwitterHandler()
        tweeter_handler.fetch_all(original_tweets_dir)

    with open(new_tweets_file, 'w', encoding='utf8') as output:
        for filename in listdir(original_tweets_dir):
            with open(path.join(original_tweets_dir, filename), encoding='utf8') as f:
                original_tweets = f.read()
                new_tweets = TweetMaker.make_tweets(original_tweets, 10)
                for new_tweet in new_tweets:
                    if not new_tweet:
                        continue

                    final_new_tweet = new_tweet + " – " + filename
                    if args.post:
                        pass  # TODO
                    output.write(final_new_tweet + '\n')
                output.write('\n')


if __name__ == '__main__':
    run()
