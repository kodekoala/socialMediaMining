#Author: Yousuf Asfari

import json
import pymongo
import sys
from collections import Counter
from prettytable import PrettyTable 
from vaderSentiment.vaderSentiment import sentiment as vaderSentiment
from art import *

try:
	conn = pymongo.MongoClient('localhost:27017')
	db = conn.cmsc491
except pymongo.errors.ConnectionFailure as e:
	print "problem connecting to cmsc491", e
	sys.exit(1)

cokeLabel=text2art("Coca-Cola")
print "\n" + cokeLabel + "\n"

#Connect to coke database, get 25 tweet structures
coke = db.CocaCola
cokeTweets = coke.find().limit(25)

#Add the unicode tweet text only to an array
cokeMessages = []
for tweet in cokeTweets:
	cokeMessages.append(tweet["text"].encode('utf-8'))

cokeTable = PrettyTable(field_names=['Tweet', 'Lexical Diversity', 'Sentiment Analysis'])

#Construct array of words for each tweet
cokeWords = []
for text in cokeMessages:
	for w in text.split():
		cokeWords.append(w)

	#Get sentiment analysis for the current tweet, as well as the lexical diversity
	vs = vaderSentiment(text)
	# print text + "\nLexical Diversity: " + str(1.0*len(set(cokeWords))/len(cokeWords)) + "\nSentiment Analysis: " + str(vs['compound']) + "\n"

	#Add a newline for better readability, and display all 25 tweets with their lex diversity and sentiment analysis in a pretty table 
	text = text + '\n'
	cokeTable.add_row([text, str(1.0*len(set(cokeWords))/len(cokeWords)), str(vs['compound'])])

	#Clear the word array for the next tweet
	del cokeWords[:]

print cokeTable


pepsiLabel=text2art("Pepsi")
print "\n" + pepsiLabel + "\n"

#Connect to pepsi database, get 25 tweet structures
pepsi = db.pepsi
pepsiTweets = pepsi.find().limit(25)

#Add the unicode tweet text only to an array
pepsiMessages = []
for tweet in pepsiTweets:
	pepsiMessages.append(tweet["text"].encode('utf-8'))

pepsiTable = PrettyTable(field_names=['Tweet', 'Lexical Diversity', 'Sentiment Analysis'])

#Construct array of words for each tweet
pepsiWords = []
for text in pepsiMessages:
	for w in text.split():
		pepsiWords.append(w)

	#Get sentiment analysis for the current tweet, as well as the lexical diversity
	vs = vaderSentiment(text)
	# print text + "\nLexical Diversity: " + str(1.0*len(set(pepsiWords))/len(pepsiWords)) + "\nSentiment Analysis: " + str(vs['compound']) + "\n"

	#Add a newline for better readability, and display all 25 tweets with their lex diversity and sentiment analysis in a pretty table 
	text = text + '\n'
	pepsiTable.add_row([text, str(1.0*len(set(pepsiWords))/len(pepsiWords)), str(vs['compound'])])

	#Clear the word array for the next tweet
	del pepsiWords[:]

print pepsiTable