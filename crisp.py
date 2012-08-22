#!/usr/bin/env python2.7
import tweetstream
import re
import urllib2
import ConfigParser
import simplejson
import sys
from datetime import datetime
from unshorten import unshorten_url
import gspread
import ConfigParser

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
first_col = wks.col_values(2)

erow = len(first_col) + 1

for url in first_col:
    print url

max_id = "226230572954038272"

# fetch the url
url = "http://search.twitter.com/search.json?q=%40dpref&rpp=100i&since_id={}".format(max_id)
json = urllib2.urlopen(url).read()
tweets = simplejson.loads(json, encoding = 'utf-8')
for tweet in reversed(tweets['results']):
    tags = re.findall(r'#(\S+)', tweet["text"])
    urls = re.findall(r'(https?://\S+)', tweet["text"])
    #Fri, 20 Jul 2012 08:17:09 +0000
    d = datetime.strptime( tweet['created_at'], '%a, %d %b %Y %H:%M:%S +0000')
    date = d.strftime('%d/%m/%Y %H:%M:%S')
    if len(urls) == 0:
        urls = [""]
    for url in urls:
        print "Processing",tweet[id]
        wks.update_cell(erow, 1, tweet['id'])
        wks.update_cell(erow, 2, date )
        wks.update_cell(erow, 3, unshorten_url(url) )
        wks.update_cell(erow, 4, ','.join(tags) )
        wks.update_cell(erow, 5, tweet['text'] )
        wks.update_cell(erow, 6, "@{}".format( tweet['from_user'] ) )
        wks.update_cell(erow, 7,  )
        wks.update_cell(erow, 8,  )
        erow += 1

