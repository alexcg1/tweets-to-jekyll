from pathlib import Path

# User tweets to get
# Todo: Convert to array for multiple streams
username = "alexcg"
tweet_limit = 200

# Filter settings
default_timeframe = 30
# TODO: hashtag_whitelist = []
exclude_replies = True
include_rts = False

## Jekyll settings

filename = 'tweets.md'
title = "Latest Tweets"

# Database
# database = 'tweets.sqlite3'

# Jekyll dir
posts_dir = './'

# Filenames

tweet_log = Path("posted_tweets.log")
