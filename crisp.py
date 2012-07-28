#!/usr/bin/env python2.7
import tweetstream
import re
import urllib2
import ConfigParser
import simplejson
import sys
from datetime import datetime
from unshorten import unshorten_url

# Force unicode behaviour:
reload(sys)
sys.setdefaultencoding('utf-8')


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
        print "\"{}\", \"{}\", \"{}\", \"{}\", \"@{}\", \"{}\"".format( date, unshorten_url(url), ','.join(tags), tweet['text'], tweet['from_user'], tweet['id'])

