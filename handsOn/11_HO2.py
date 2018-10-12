from collections import Counter
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
import pymongo
import sys

try:
	conn = pymongo.MongoClient('localhost:27017')
	db = conn.cmsc491
except pymongo.errors.ConnectionFailure as e:
	print "problem connecting to cmsc491", e
	sys.exit(1)

hlc = db.antarctica
tweets = hlc.find({"lang":"en"})

desc = []
for tweet in tweets:
	if (tweet["user"]["description"] is not None):
		vs = vaderSentiment(tweet["user"]["description"].encode('utf-8'))
		print "\n\t" + str(vs['compound'])
		print tweet["user"]["description"].encode('utf-8')
		print "======================================"
		desc.append(tweet["user"]["description"])