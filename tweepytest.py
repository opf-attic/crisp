import tweepy
import ConfigParser
import sys

# Force unicode behaviour:
reload(sys)
sys.setdefaultencoding('utf-8')


# == OAuth Authentication ==
config = ConfigParser.ConfigParser()
config.read("config.ini")

#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key=config.get("twitter", "consumer_key")
consumer_secret=config.get("twitter", "consumer_secret")

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token=config.get("twitter", "access_token")
access_token_secret=config.get("twitter", "access_token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print api.me().name

for status in api.mentions():
    print "@{}".format(status.user.screen_name)
    for property, value in vars(status).iteritems():
        print property, ": ", value

