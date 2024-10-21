import tweepy
import os
import sys

sys.path.append('..')

from config import BEARER_TOKEN, api_key, api_key_secret, access_token, access_token_secret  # Import token from config.py


# Authenticate
auth = tweepy.OAuthHandler(api_key, api_key_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)


def get_user_tweets(username, tweet_count=10):
    # Get the user ID from the username
    tweets = api.user_timeline(screen_name=username, count=tweet_count,
                           tweet_mode='extended')
    # Print the tweets
    for tweet in tweets.data:
        print(f"{tweet.id}: {tweet.text}")

    return tweets
# Example usage
get_user_tweets(username='AIForTrading1', tweet_count=28)

