#!/usr/bin/env python3

import twitter
import re
from datetime import datetime, timedelta

try:
    import config
except:
    print("Error: No config file found")


def get_tweets():
    api = twitter.Api(
        consumer_key = config.consumer_key,
        consumer_secret = config.consumer_secret,
        access_token_key = config.access_token_key,
        access_token_secret = config.access_token_secret)

    username = config.username
    tweets = api.GetUserTimeline(screen_name=username, exclude_replies=True)
    return tweets


def filter_tweets(tweets, timeframe=config.default_timeframe):
    filtered_tweets = []
    timeframe = datetime.combine(datetime.now().date() - timedelta(days = timeframe),datetime.min.time())
    for tweet in [s for s in tweets]:
        tweet_year = tweet.created_at[-4:]
        tweet_date = tweet.created_at[:-20]
        tweet_date = tweet_date + ' ' + tweet_year
        tweet_date = datetime.strptime(tweet_date, '%a %b %d %Y')
        if tweet_date >= timeframe:
            filtered_tweets.append(tweet)
    return(filtered_tweets)


def format_tweets(tweets):
    formatted_tweet_list = []
    url_format = ' https:\/\/t.co\/.*'
    rt_format = r'RT @.*:'

    for tweet in [s for s in tweets]:
        text = tweet.text.replace("\n", " ")
        text = re.sub(url_format, '', text, flags=re.MULTILINE)
        via = re.findall(rt_format, text)
        text = re.sub(rt_format+' ', '', text)

        if tweet.quoted_status:
            url = tweet.quoted_status.urls[0].url
        elif tweet.urls:
            url = tweet.urls[0].url

        formatted_tweet = f"* [{text}]({url})"

        if via:
            via = re.sub('RT ', '', via[0])
            via = ' via ' + re.sub(':', '', via)
            formatted_tweet += via

        formatted_tweet_list.append(formatted_tweet)

    return formatted_tweet_list


def write_tweets_to_file(tweets):
    header = f"---\ntitle: {config.title}\n---\n\n"
    footer = "\nCreated with tweets-to-jekyll"
    count = 0
    body = ''

    for tweet in tweets:
        body += tweet+'\n'
        count += 1

    with open(config.filename, "w") as file:
        file.write(header)
        file.write(body)
        file.write(footer)

    print(f"{count} tweets written to {config.filename}")


def post_to_jekyll(tweets):
    pass


if __name__ == "__main__":
    tweets = get_tweets()
    tweets = filter_tweets(tweets)
    tweets = format_tweets(tweets)

    write_tweets_to_file(tweets)

