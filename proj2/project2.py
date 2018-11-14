import russell as ru

from bs4 import BeautifulSoup
import requests
import json
import codecs
import nltk
import string

#Add Unicode filter
def removeUnicode(text):
	asciiText = ""
	for char in text:
		if (ord(char) < 128):
			asciiText = asciiText + char
	return asciiText

#Open file we can write the text of our web page to
fileObj = codecs.open("project2.rtf", "w", "UTF")

#Get a web page
html = requests.get("http://www.ecommercetimes.com/story/52616.html")

soup = BeautifulSoup(html.text, 'html5lib')

#Get the text in the p tag for this site based on recon

all_paras = soup.find_all('p')

#Write text to file and collate it into a str var
data = ""
for para in all_paras:
	fileObj.write(para.text)
	data = data + para.text

#Call the russel luhn summarization function
luhn_sum = ru.summarize(data)

#Print the results
print "Three Sentence Summary:" + "\n"
for sent in luhn_sum['top_n_summary']:
	print removeUnicode(sent) + '\n'

asc = removeUnicode(data)

#We need a list of words by sentence to feed into our searcher
bigWords = nltk.tokenize.word_tokenize(asc)

#We need to designate the number of collocations to find 
N = 25
#Lets have the nltk analyze our sentWords for collocations with a searcher
search = nltk.BigramCollocationFinder.from_words(bigWords)

#Now filter out collocations that do not occur at least 2 times
search.apply_freq_filter(2)

#And filter out collocations that have stopwords
search.apply_word_filter(lambda skips: skips in nltk.corpus.stopwords.words('English'))

#Use the Jaccard Index to find our bigrams
from nltk import BigramAssocMeasures
idxJaccard = BigramAssocMeasures.jaccard 
bigrams = search.nbest(idxJaccard, N)

#Now lets print the results
print "Bigrams found:" + "\n"
for bigram in bigrams:
	#Filter out punctuation and unnecessary bigrams that present no value to us
	bigram1 = (str(bigram[0]).encode('utf-8') + " ").translate(None, string.punctuation)
	bigram2 = str(bigram[1]).encode('utf-8').translate(None, string.punctuation)

	if (bigram1 != " " and bigram2 != " "):
		print (bigram1 + bigram2)


