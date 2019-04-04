# Politibot
Create tweets that sound like Israeli politicians

You can see the bot in action here: https://twitter.com/Politibot14

Politibot takes recent politicians' tweets, creates a Markov chain from them, and tries to create a tweet that sounds like something they'd tweet.

## Usage
1. Clone the repository, create a conda environment based on `environment.yml` and activate it
2. Create a config file: `twitter_config.json` in the config directory based on the following template (consult Twitter API docs for more details):
```json
{
  "consumer_key": "<twitter_consumer_key>",
  "consumer_secret": "<twitter_consumer_secret>",
  "access_token": "<twitter_access_token>",
  "access_token_secret": "<twitter_access_token_secret>",
  "max_pages": 1000
}
```
3. Run `src/politibot/main.py`:
```bash
python /home/gil/PycharmProjects/politibot/src/politibot/main.py --fetch
``` 