import markovify


class TweetMaker:
    @staticmethod
    def make_tweets(text, count):
        text_model = markovify.Text(text)
        return [text_model.make_short_sentence(240) for _ in range(count)]
