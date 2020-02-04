# Tweets to Jekyll

Small Python program to grab your tweets, collect them in a bulleted list, and post to your [Jekyll](https://jekyllrb.com/) site. Still a work in progress so expect bugs and limited features for now

## Installation

### Install prerequisites

```
pip install -r requirements.txt
```

### Set up credentials and config

* Edit sample.credentials.py and save as *credentials.py*. You'll need to sign up as a Twitter developer to get API key, etc. Your username, etc can be set in config.py.
* Edit config.py to specify username, blog directory, etc

## Usage

Run `./tweets-to-jekyll.py` to shunt your tweets into a markdown file.

## TODO

[Check the todo file](TODO.md)

## Troubleshooting

### These aren't my tweets!

Edit the `username` variable in *config.py*
