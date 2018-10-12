import json
import pymongo
import sys

try:
	conn = pymongo.MongoClient('localhost:27017')
	db = conn.cmsc491
except pymongo.errors.ConnectionFailure as e:
	print "problem connecting to cmsc491", e
	sys.exit(1)

hlc = db.antarctica
tweets = hlc.find()

print"==============================="

if tweets[1]["user"]:
	print tweets[1]["user"].keys()
	print tweets[1]["user"]["screen_name"].encode('utf-8')
	print tweets[1]["user"]["description"].encode('utf-8')
	print tweets[1]["user"]["location"].encode('utf-8')
	print"==============================="
else:
	print "no user data this go round"