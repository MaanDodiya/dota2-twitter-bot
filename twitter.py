import app
import tweepy

# Refer: http://docs.tweepy.org/en/latest/auth_tutorial.html#oauth-1a-authentication
auth = tweepy.OAuthHandler("consumer_key", "consumer_secret")
auth.set_access_token("key", "secret")

api = tweepy.API(auth, wait_on_rate_limit=True,
                 wait_on_rate_limit_notify=True)
user = api.me()

tweets = app.compileTweet()

if(tweets != False):
    for tweet in tweets:
        api.update_status(tweet)
