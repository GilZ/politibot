import markovify


def make_tweets_from_model(model, count):
    return [model.make_short_sentence(240) for _ in range(count)]


def make_tweets_from_text(text, count):
    model = markovify.Text(text)
    return make_tweets_from_model(model, count), model


def combine(combined_model, model):
    if combined_model is None:
        return model
    return markovify.combine(models=[combined_model, model])
