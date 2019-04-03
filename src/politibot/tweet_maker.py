import markovify


class TweetMaker:
    @staticmethod
    def make_tweet(text):
        text_model = markovify.Text(text)
        return text_model.make_short_sentence(280)

# Get raw text as string.
# with open("/home/gil/richness/bibi.txt") as f:
#     text = f.read()

# Build the model.
# text_model = markovify.NewlineText(text)

# Print five randomly-generated sentences
# for i in range(5):
#     print(text_model.make_sentence())

# Print three randomly-generated sentences of no more than 140 characters
# for i in range(3):
# print(text_model.make_short_sentence(280))