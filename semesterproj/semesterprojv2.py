from nltk.tokenize import word_tokenize
from nltk import pos_tag
from nltk.chunk import ne_chunk
import wikipedia
import rdflib
import russell as ru
from bs4 import BeautifulSoup
import requests
import json
import codecs
import nltk
import string
from nltk import BigramAssocMeasures

#Define topic
e = ""
topic = "Nvidia"

try:
	entity = str(wikipedia.summary(topic, sentences = 4).encode('utf-8'))
	entity = entity.decode('utf-8')
	#Now  apply  the NLP processes to define tokens, parts of speech and then we can get entities and phrases
	tokens = word_tokenize(entity)
	gmrTags = pos_tag(tokens)
	gmrChunks = ne_chunk(gmrTags, binary = True)

	#Let's print the summary
	print("Topic summary {}".format(topic))
	print(entity)
	print("====")

	#We can derive noun phrases
	print("Topic has these noun phrases in 4 sentence summary:")
	gmrNouns = []
	gmrPrev = None
	gmrPhrase = []
	for (token, pos) in gmrTags:
		if pos.startswith('NN'):
			if pos == gmrPrev:
				gmrPhrase.append(token)
			else:
				if gmrPhrase:
					gmrNouns.append((''.join(gmrPhrase), gmrPrev))
				gmrPhrase = [token]
		else:
			if gmrPhrase:
				gmrNouns.append((''.join(gmrPhrase), gmrPrev))
			gmrPhrase = []
			gmrPrev = pos
		
	if gmrPhrase:
		gmrNouns.append((''.join(gmrPhrase), pos))

	for noun in gmrNouns:
		print(noun[0])
	print("====")

	print("Topic summary has these named entities, with description:")
	typeEntity = 'NE'
	gmrEntity = []
	for gmrNE in gmrChunks.subtrees():
		if gmrNE.label() == typeEntity:
			tokens = [t[0] for t in gmrNE.leaves()]
			gmrEntity.append(tokens[0])

	#Undup the named entities
	gmrList = []
	for gmrNE in gmrEntity:
		gmrList.append(gmrNE)
	gmrSet = set(gmrList)

	#Now loop thru the set and find the meanings of the NE's
	for item in gmrSet:
		print item
		try:
			summary = wikipedia.summary(item, sentences = 1)
			print("{}: {}".format(item, summary.encode('utf-8')))
		except wikipedia.exceptions.WikipediaException as e1:
			print "This NE has multiple meanings in wikipedia"
			continue

	#If our main topic needs disambiguation, print out the list of potential meanings from the exception
except wikipedia.exceptions.WikipediaException as e:
	print e
	print "Wikipedia says to disambiguate"

print('\n\n')
###########################################################
print "###########################################################\n"

#Now use dbpedia
entity = "Nvidia"

dbpedia_url = 'http://dbpedia.org/resource/{}'.format(entity)

#groups of rdf statements are organized into graphs. our first rdf step is to create an rdf graph isntance
#and then populate it with rdf triples based on our topic
grf = rdflib.Graph()
grf.parse(dbpedia_url)

#We need to disambiguate our topic, which is to say that we need to find out if it refers to multiple topics
query = (rdflib.URIRef(dbpedia_url),
	rdflib.URIRef('http://dbpedia.org/ontology/wikiPageDisambiguates'),
	None)

multiples = list(grf.triples(query))

#If we find multiple meanings then print them out
if len(multiples) > 1:
	print("Your topic {}:".format(dbpedia_url))
	for subject, verb, object in multiples:
		print('----can mean : {}'.format(object))
else:
	query = (rdflib.URIRef(dbpedia_url),
			rdflib.URIRef('http://dbpedia.org/ontology/abstract'),
			None)
	summary = list(grf.triples(query))
	for subject, verb, object in summary:
		if object.language == 'en':
			print(object.encode('utf-8'))

print "###########################################################\n"
print('\n\n')
###########################################################

#Part 2, summarizations and Bigrams

#Add Unicode filter
def removeUnicode(text):
	asciiText = ""
	for char in text:
		if (ord(char) < 128):
			asciiText = asciiText + char
	return asciiText


listofsites = [
'https://blogs.nvidia.com/blog/2018/06/20/nvidia-chief-scientist-bill-dally-on-how-gpus-ignited-ai-and-where-his-teams-headed-next/',
'https://blogs.nvidia.com/blog/2018/11/06/rsna-radiology-transformation-ai/',
'https://blogs.nvidia.com/blog/2018/10/31/deep-learning-mammogram-assessment/',
'https://blogs.nvidia.com/blog/2018/10/29/planck-ai-ships-strikes-right-whales/'
]

counter = 1
headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/60.0.3112.113 Safari/537.36'}

for  website in listofsites:

	#Open file we can write the text of our web page to
	fileObj = codecs.open("website" + str(counter) + ".rtf", "w", "UTF")
	#Get a web page
	html = requests.get(website, headers=headers)
	soup = BeautifulSoup(html.text, 'html.parser')
	all_paras = soup.find('div',attrs={"class":"has-content-area"}).findAll('p')

	#Write text to file and collate it into a str var
	data = ""
	for para in all_paras:
		fileObj.write(para.text)
		data = data + para.text
	del all_paras[:]

	#Call the russel luhn summarization function
	luhn_sum = ru.summarize(data)

	#Print the results
	print "Three Sentence Summary for Website #" + str(counter) + ":" + "\n"
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
	idxJaccard = BigramAssocMeasures.jaccard 
	bigrams = search.nbest(idxJaccard, N)

	#Now lets print the results
	print "Bigrams found:" + "\n"
	for bigram in bigrams:
		#Filter out punctuation and unnecessary bigrams that present no value to us
		bigram1 = (str(bigram[0]).encode('utf-8') + " ").translate(None, string.punctuation)
		bigram2 = str(bigram[1]).encode('utf-8').translate(None, string.punctuation)

		if (bigram1.replace(" ", "").isalnum() and bigram2.replace(" ", "").isalnum()):
			print (bigram1 + bigram2)
	print('\n')

	counter += 1