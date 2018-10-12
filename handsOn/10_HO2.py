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
texts = []
for status in tweets:
	texts.append(status["text"])
print texts

print"==============================="

words = []
for text in texts:
	print text.encode('utf-8')
	for w in text.split():
		words.append(w)

print words

cnt = Counter(words)

pt = PrettyTable(field_names=['Word', 'Count'])
srtCnt = sorted(cnt.items(), key=lambda pair: pair[1], reverse=True)

for kv in srtCnt:
	pt.add_row(kv)
print pt

print"==============================="


print "Lexical Diversity"
print 1.0*len(set(words))/len(words)