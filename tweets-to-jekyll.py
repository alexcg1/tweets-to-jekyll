#!/usr/bin/env python3

from pathlib import Path
import sys
import config
import logging as log
from datetime import datetime, timedelta

log.basicConfig(format="* %(levelname)s: %(message)s", level=log.INFO)

simple_tweets = []
tweets_written = 0
tweets_skipped = 0


def get_tweets():
    '''
    Get tweets from user account
    '''
    import credentials
    import twitter

    try:
        get_last_tweet_id()
    except:
        pass

    api = twitter.Api(
        consumer_key = credentials.consumer_key,
        consumer_secret = credentials.consumer_secret,
        access_token_key = credentials.access_token_key,
        access_token_secret = credentials.access_token_secret)

    try:
        tweets = api.GetUserTimeline(
            screen_name=config.username,
            exclude_replies=config.exclude_replies,
            count=config.tweet_limit
        )
        log.info(f"{len(tweets)} tweets received from {config.username}")
    except:
        log.warn("Failed to retrieve tweets")

    return tweets


def __get_last_tweet_id():
    '''
    Get the id field of the user's most recent tweet from the log
    '''

    if config.tweet_log.is_file:
        with open(config.tweet_log, "r") as file:
            tweet_id = file.readlines()[0]

    return tweet_id


def filter_tweets(tweets, timeframe=config.default_timeframe):
    '''
    Filter tweets based on timeframe and (pending) other criteria
    '''
    filtered_tweets = []
    timeframe = datetime.combine(datetime.now().date() - timedelta(days = timeframe),datetime.min.time())
    for tweet in [s for s in tweets]:
        tweet.done = False
        tweet_year = tweet.created_at[-4:]
        tweet_date = tweet.created_at[:-20]
        tweet_date = tweet_date + ' ' + tweet_year
        tweet_date = datetime.strptime(tweet_date, '%a %b %d %Y')
        if tweet_date >= timeframe:
            filtered_tweets.append(tweet)
    return(filtered_tweets)


def format_tweets(tweets):
    '''
    Convert tweet dict to array of markdown bullet points
    '''
    import re
    formatted_tweet_list = []
    url_format = ' https:\/\/t.co\/.*'
    rt_format = r'RT @.*:'
    counter = 0

    for tweet in [s for s in tweets]:
        text = tweet.text.replace("\n", " ")
        text = re.sub(url_format, '', text, flags=re.MULTILINE)
        via = re.findall(rt_format, text)
        text = re.sub(rt_format+' ', '', text)

        # Set default url
        tweet.url = f"https://twitter.com/{config.username}/statuses/{tweet.id}"

        # Better URL handling - get direct link if link mentioned in tweet (e.g. to YouTube or whatever)
        # if tweet.media:
        # print("Media")
        # # url = tweet.retweeted_status.urls[0].url
        # print(tweet.id_str)
        # url = ''
        # elif tweet.retweeted_status:
        # print("Retweet")
        # # url = tweet.retweeted_status.urls[0].url
        # print(tweet.retweeted_status.media)
        # url = ''
        # elif tweet.quoted_status:
        # try:
        # url = tweet.quoted_status.urls[0].url
        # except:
        # url = ''
        # elif tweet.urls:
        # url = tweet.urls[0].url
        # else:
        # url = ''

        tweet.formatted = f"* [{text}]({tweet.url})"

        if via:
            via = re.sub('RT ', '', via[0])
            via = ' via ' + re.sub(':', '', via)
            tweet.formatted += via
            tweet.via = via

        simple_tweet = {"id": tweet.id, "url": tweet.url, "text": tweet.text, "formatted": tweet.formatted, "timestamp": 0, "done": False}

        simple_tweets.append(simple_tweet)


def write_tweets_to_file(simple_tweets, file=config.filename):
    '''
    Write header, footer, and each bullet point to a markdown file, based on contents of simple dict of twitter data.
    '''
    header = f"---\ntitle: {config.title}\n---\n\n"
    footer = "\n[Created with tweets-to-jekyll](https://github.com/alexcg1/tweets-to-jekyll)"
    count = 0
    skipped_count = 0
    body = ''

    for tweet in simple_tweets:
        if __check_log_for_tweet(tweet) == True:
            skipped_count += 1
            pass
        else:
            body += tweet["formatted"]+'\n'
            count += 1
            __write_log(tweet)

    if count > 0:
        with open(config.filename, "w") as file:
            file.write(header)
            file.write(body)
            file.write(footer)

        log.info(f"{count} tweets written to {config.filename}. {skipped_count} tweets skipped (already posted)")
    else:
        log.info(f"No new tweets to write to {config.filename}")


def post_to_jekyll(file):
    '''
    Move the file to your jekyll posts directory
    '''
    pass


def __check_log_for_tweet(tweet):
    '''
    Check if tweet already logged in file
    '''
    if config.tweet_log.is_file:
        with open(config.tweet_log, "r") as file:
            if str(tweet["id"])+"\n" in file.readlines():
                return True

    return False


def __write_log(tweet):
    '''
    Mark tweet as processed in the database
    '''
    if __check_log_for_tweet(tweet) == True:
        pass

    else:
        with open("posted_tweets.log", "a") as file:
            file.write(str(tweet["id"])+"\n")


if __name__ == "__main__":

    # mark_posted()
    tweets = get_tweets()
    filtered_tweets = filter_tweets(tweets)
    formatted_tweets = format_tweets(filtered_tweets)
    # pprint(simple_tweets)
    # write_tweets_to_file(formatted_tweets)
    write_tweets_to_file(simple_tweets)
    # print(f"{tweets_written} tweets written to {config.filename}. {tweets_skipped} skipped")

