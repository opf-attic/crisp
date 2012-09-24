#!/usr/bin/env python
import gspread
import ConfigParser
import tweepy
import sys
import re
from datetime import datetime
from unshorten import unshorten_url

# Force unicode behaviour:
reload(sys)
sys.setdefaultencoding('utf-8')

config = ConfigParser.ConfigParser()
config.read("config.ini")
guser = config.get("google", "user")
gpw = config.get("google", "pw")

# Login with your Google account
gc = gspread.login(guser, gpw)

# Open a worksheet from spreadsheet
ss = gc.open("CRISP Data Collection Form")
#wks = ss.sheet1 # Submissions sheet
wks = ss.get_worksheet(1) # Tweets sheet

# Get all values from column. Column and row indexes start from one
first_col = wks.col_values(1)

erow = len(first_col) + 1

max_id = 0

for tid in first_col:
    if tid == None or tid == "ID":
        continue
    if int(tid) > max_id:
        max_id = int(tid)

# Twitter:
# == OAuth Authentication ==
consumer_key=config.get("twitter", "consumer_key")
consumer_secret=config.get("twitter", "consumer_secret")
access_token=config.get("twitter", "access_token")
access_token_secret=config.get("twitter", "access_token_secret")

auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)

api = tweepy.API(auth)

# If the authentication was successful, you should
# see the name of the account print out
#print api.me().name

# fetch the tweets
for status in reversed(api.mentions()):
    if status.id <= max_id:
        print "Skipping", status.id, max_id - status.id
        continue
    user = "@{0}".format(status.user.screen_name)
    tags = re.findall(r'#(\S+)', status.text)
    urls = re.findall(r'(https?://\S+)', status.text)
    #Fri, 20 Jul 2012 08:17:09 +0000
    d = status.created_at
    date = d.strftime('%d/%m/%Y %H:%M:%S')
    if len(urls) == 0:
        urls = [""]
    for url in urls:
        print "Processing",status.id
        wks.update_cell(erow, 1, str(status.id) )
        wks.update_cell(erow, 2, date )
        wks.update_cell(erow, 3, unshorten_url(url) )
        wks.update_cell(erow, 4, ','.join(tags) )
        wks.update_cell(erow, 5, status.text )
        wks.update_cell(erow, 6, user )
        #wks.update_cell(erow, 7,  )
        #wks.update_cell(erow, 8,  )
        erow += 1

