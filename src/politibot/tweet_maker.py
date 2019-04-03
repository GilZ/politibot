import markovify


class TweetMaker:
    @staticmethod
    def make_tweet(text):
        text_model = markovify.NewlineText(text)
        return text_model.make_short_sentence(280)
