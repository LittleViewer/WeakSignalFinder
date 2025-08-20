import feedparser
import time
import nltk
import os
nltk_data_dir = os.path.join(os.getcwd(), "nltk_data")
os.makedirs(nltk_data_dir, exist_ok=True)
nltk.data.path.append(nltk_data_dir)
resources = [
    'punkt',
    'punkt_tab',
    'wordnet',
    'averaged_perceptron_tagger',
    'averaged_perceptron_tagger_eng'
]
for r in resources:
    try:
        nltk.data.find(r)
    except LookupError:
        nltk.download(r, download_dir=nltk_data_dir, quiet=True)
from nltk.stem import WordNetLemmatizer
import re
from intensityContext import intensityContext

def presenceWord(word, wordIntensity):
    isExist = False
    index = 0
    for p in range(len(wordIntensity)):
        if wordIntensity[p][0] == word :
            isExist = True
            index = p

    if isExist == False:
        wordIntensity.append([word, 1])
    else :
        contentValue = wordIntensity[index][1]
        wordIntensity[index][1] = contentValue + 1
    
    return wordIntensity

def wordInsentyPrintImportantRepresent(wordIntensity) :
    for l in range(len(wordIntensity)):
        if wordIntensity[l][1] >= 5:
            print(wordIntensity[l])

def parseRss(file="rss.txt"):
    arrayNewFeed = []
    nameRssSender = []
    with open(file, "r") as stream:
        arrayFileContent = [line.strip() for line in stream if line.strip()]
    for line in arrayFileContent:
        arrayNewFeed.append(feedparser.parse(line))
        parts = line.split(".")
        if len(parts) > 1:
            nameRssSender.append(WordNetLemmatizer().lemmatize(parts[1]))
        else:
            print("URL ignorée (pas de point) :", line)
    return [arrayNewFeed, set(nameRssSender)]


def stopWordUsual(file = "stopword.txt"):
    stream = open(file, "r")
    arrayStopWord = stream.read()
    return set(arrayStopWord.split("\n"))

def saveContext(word, index, content, contextWord, setStopWordUsual):
    beforeRealise = False
    if (index-1) >= 0 :
        if  re.match('^(?!nbsp$)[A-Za-z0-9]+$', content[index - 1][0].lower()) :
            if content[index - 1][0].lower() in setStopWordUsual:
                pass
            else:
                beforeWord = [content[index - 1][0].lower(), word.lower()]
                beforeRealise = True
    
    if len(content) > (index+1) and beforeRealise == True :
        if  re.match('^(?!nbsp$)[A-Za-z0-9]+$', content[index + 1][0].lower()) :
            if content[index + 1][0].lower() in setStopWordUsual:
                pass
            else :
                beforeWord.append(content[index + 1][0].lower())
                contextWord.append(beforeWord)
    elif len(content) > (index+1) and beforeRealise == False:
        if  re.match('^(?!nbsp$)[A-Za-z0-9]+$', content[index + 1][0].lower()) :
            if content[index + 1][0].lower() in setStopWordUsual:
                pass
            else :
                contextWord.append([word.lower(), content[index + 1][0].lower()])
    elif beforeRealise == True:
        contextWord.append(beforeWord)
    return contextWord



arrayStopWordUsual = stopWordUsual()
arrayOutputParseRss = parseRss()
contexWordSave = []
arrayNewFeed = arrayOutputParseRss[0]
nameRssOrganisationSender = arrayOutputParseRss[1]
wordIntensity = [["a", 1]]



for x in range(len(arrayNewFeed)):
    for i in range(len(arrayNewFeed[x].entries)):
        #print(arrayNewFeed[x].entries[i]["title"])
        #print(time.strftime("%Y-%m-%d %H:%M:%S", arrayNewFeed[x].entries[i]["published_parsed"]))
        #print(arrayNewFeed[x].entries[i]["summary"])
        #print("\ \ \ \ ")
        tokenizePost = list(nltk.word_tokenize(arrayNewFeed[x].entries[i]["title"]) + list(nltk.word_tokenize(arrayNewFeed[x].entries[i]["summary"])))
        tagTokenizePost = nltk.pos_tag(tokenizePost)
        for j in range(len(tagTokenizePost)) :
            tag = tagTokenizePost[j][1]
            word = (tagTokenizePost[j][0]).lower()
            if tag.startswith("NN") and re.match('^(?!nbsp$)[A-Za-z0-9]+$', word) and len(word) > 1 : 
                lemWord = WordNetLemmatizer().lemmatize(word)
                isOrganisationSenderRss = False
                isUsualStopWord = False
                if lemWord in nameRssOrganisationSender :
                    isOrganisationSenderRss = True
                if lemWord in arrayStopWordUsual:
                    isUsualStopWord = True
                if isOrganisationSenderRss == False and isUsualStopWord == False :       
                    wordIntensity = presenceWord(lemWord, wordIntensity)
                    contexWordSave = saveContext(lemWord, j, tagTokenizePost, contexWordSave, arrayStopWordUsual)
                                    


wordInsentyPrintImportantRepresent(wordIntensity)
#print(nameRssOrganisationSender)
#print(contexWordSave)

objIntensityContext = intensityContext(contexWordSave)
contextNumber = objIntensityContext.returnValue()
for u in range(len(contextNumber)):
    if type(contextNumber[u][2]) == int:
        number = 2
    elif type(contextNumber[u][3]) == int:
        number = 3 

    if number == 2 :
        if contextNumber[u][2] > 2 :
            print(contextNumber[u])
    elif number == 3:
        if contextNumber[u][3] > 0 :
            print(contextNumber[u])

thematicContext(contextNumber)










