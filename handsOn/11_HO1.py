import json
import pymongo
import sys
from collections import Counter
from prettytable import PrettyTable

try:
	conn = pymongo.MongoClient('localhost:27017')
	db = conn.cmsc491
except pymongo.errors.ConnectionFailure as e:
	print "problem connecting to cmsc491", e
	sys.exit(1)

hlc = db.antarctica
tweets = hlc.find()
g = open('gmrTweet.txt', 'w')

retweets = []

for status in tweets:
	if 'retweeted_status' in status:
		retweets.append((status['user']['screen_name'], status['retweeted_status']['user']['screen_name'], status['text']))
		g = open('gmrTweet.txt', 'w')
		g.write(str(status))
		g.close()

pt = PrettyTable(field_names=['Usr', 'rtUsr', 'Text'])
[pt.add_row(row) for row in sorted(retweets, reverse = True)[:5]]
pt.max_width['Text'] = 40
pt.align = 'l'
print pt