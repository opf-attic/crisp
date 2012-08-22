import tweepy


# == OAuth Authentication ==
#
# This mode of authentication is the new preferred way
# of authenticating with Twitter.

# The consumer keys can be found on your application's Details
# page located at https://dev.twitter.com/apps (under "OAuth settings")
consumer_key="ZQss1qDPr7KGs1zHXGd77w"
consumer_secret="2sGShNrgMKbCqSiAkvlrj7xNwW8eTfArm40ywxiT3To"

# The access tokens can be found on your applications's Details
# page located at https://dev.twitter.com/apps (located 
# under "Your access token")
access_token="561459521-3xN03j1PEJvVhF9BFUKBOY4cAuJU7a74rnRFToo"
access_token_secret="DytWB5VC28wB1vIFS1QrhoMcjkXi04m3ef3z5bv7b0"

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
print api.me().name

for status in api.mentions():
    print "NAME", status.user.screen_name
    for property, value in vars(status).iteritems():
        print property, ": ", value

