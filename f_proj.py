#Final Project..
import json
import codecs
import nltk
from nltk import BigramAssocMeasures
from bs4 import BeautifulSoup
import requests
import russell as ru
import string



link1 = "https://blogs.nvidia.com/blog/2018/06/20/nvidia-chief-scientist-bill-dally-on-how-gpus-ignited-ai-and-where-his-teams-headed-next/"
link2 = "https://blogs.nvidia.com/blog/2018/11/06/rsna-radiology-transformation-ai/"
link3 = "https://blogs.nvidia.com/blog/2018/10/31/deep-learning-mammogram-assessment/"
link4 ="https://blogs.nvidia.com/blog/2018/10/29/planck-ai-ships-strikes-right-whales/"

sites = [link1, link2, link3, link4]
import json
import codecs
import nltk
from nltk import BigramAssocMeasures


def removeUnicode(text):
    asciiText = ""
    for char in text:
        if (ord(char) < 128):
            asciiText = asciiText + char
    return asciiText


def sumFile(site):
    html = requests.get(site)
    soup = BeautifulSoup(html.text, "html5lib")
    all_paras = soup.find_all("p")
    data = ""
    for para in all_paras:
        data = data + para.text

    summary = ru.summarize(data)
    print "Summary of " + site + "\n"

    for sent in summary["top_n_summary"]:
        print removeUnicode(sent).replace(u"Friend's Email Address\n\t\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tYour Name\n\t\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tYour Email Address\n\t\t\t\t\t\n\t\t\t\t\n\t\t\t\t\tComments\n\t\t\t\t\t\n\t\t\t\t\n\t\t\t\t\t Send Email", "")

    asc = removeUnicode(data)

    # We need a list of words by sentence to feed into our searcher
    bigWords = nltk.tokenize.word_tokenize(asc)

    # We need to designate the number of collocations to find
    N = 25
    # Lets have the nltk analyze our sentWords for collocations with a searcher
    search = nltk.BigramCollocationFinder.from_words(bigWords)

    # Now filter out collocations that do not occur at least 2 times
    search.apply_freq_filter(2)

    # And filter out collocations that have stopwords
    search.apply_word_filter(lambda skips: skips in nltk.corpus.stopwords.words('English'))

    # Use the Jaccard Index to find our bigrams
    from nltk import BigramAssocMeasures
    idxJaccard = BigramAssocMeasures.jaccard
    bigrams = search.nbest(idxJaccard, N)

    # Now lets print the results
    print "Bigrams found:" + "\n"
    for bigram in bigrams:
        # Filter out punctuation and unnecessary bigrams that present no value to us
        bigram1 = (str(bigram[0]).encode('utf-8') + " ").translate(None, string.punctuation)
        bigram2 = str(bigram[1]).encode('utf-8').translate(None, string.punctuation)

        if (bigram1 != " " and bigram2 != " "):
            print (bigram1 + bigram2)
    print "\n"

def main():
    for x in sites:
        sumFile(x);
        print "-----------------------------------------------------------------------------"

main()


