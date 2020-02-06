from datetime import date

# Todo: Convert to array for multiple streams
username = "alexcg"
jekyll_folder = "/home/alexcg/code/alexcg1.github.io/_posts"
tags = "twitter" # Comma separated list
tweet_limit = 200

# Filter settings
default_timeframe = 30
# TODO: hashtag_whitelist = []
exclude_replies = True
include_rts = False

## Jekyll settings

title = f"Tweets"

# Filenames
post_filename = f"{date.today()}-tweets.md"
tweet_log = "posted_tweets.log"
