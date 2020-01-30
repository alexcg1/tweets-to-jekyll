#!/usr/bin/env python3

import twitter
import config
import re
from datetime import datetime, timedelta

def get_tweets(timeframe = config.default_timeframe):
    api = twitter.Api(
        consumer_key = config.consumer_key,
        consumer_secret = config.consumer_secret,
        access_token_key = config.access_token_key,
        access_token_secret = config.access_token_secret)

    username = config.username
    statuses = api.GetUserTimeline(screen_name=username, exclude_replies=True)

    formatted_tweet_list = []

    timeframe = datetime.combine(datetime.now().date() - timedelta(days = timeframe),datetime.min.time())

    # Regexes to find RT's and tweets w/ URLs

    tweets = filter_tweets(statuses)

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

    for tweet in formatted_tweet_list:
        print(tweet)
    return formatted_tweet_list

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

def format_tweet(tweet):
    pass

def write_tweets_to_file(tweets):
    count = 0
    with open('tweets.md', "w") as file:
        for tweet in tweets:
            file.write(tweet+'\n')
            count += 1
        print(count, "tweets written to file")

tweets = get_tweets()
write_tweets_to_file(tweets)

