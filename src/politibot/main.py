from twitter_handler import TwitterHandler
import tweet_maker
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

    twitter_users = config_manager.get_config('twitter_users')
    combined_model = None
    with open(new_tweets_file, 'w', encoding='utf8') as output:
        for filename in listdir(original_tweets_dir):
            with open(path.join(original_tweets_dir, filename), encoding='utf8') as f:
                original_tweets = f.read()
                new_tweets, model = tweet_maker.make_tweets_from_text(original_tweets, 10)
                combined_model = tweet_maker.combine(combined_model, model)
                output_tweets(new_tweets, filename, twitter_users[filename], output)
        new_combined_tweets = tweet_maker.make_tweets_from_model(combined_model, 20)
        output_tweets(new_combined_tweets, config['bot_screen_name'], config['bot_name'], output)


def output_tweets(tweets, handle, name, output):
    for new_tweet in tweets:
        if not new_tweet:
            continue

        final_new_tweet = '{name} ({handle}): {tweet}'.format(name=name, handle=handle, tweet=new_tweet)

        output.write(final_new_tweet + '\n')
    output.write('\n')


if __name__ == '__main__':
    run()
