import feedparser
import matplotlib.pyplot
import nltk
import spacy
import re
import os
from nltk.stem import WordNetLemmatizer
from intensityContext import intensity_context
from intensityContext import thematic_context
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

nlp = spacy.load("en_core_web_sm")

#Vas dans le fichier rss.txt l'ensemble des flux rss définit part l'user
def parseRss(file="rss.txt"):
    array_new_feed = []
    name_rss_sender = []
    with open(file, "r") as stream:
        array_file_content = [line.strip() for line in stream if line.strip()]
    for line in array_file_content:
        try:
            array_new_feed.append(feedparser.parse(line))
            parts = line.split(".")
            if len(parts) > 1:
                name_rss_sender.append(WordNetLemmatizer().lemmatize(parts[1]))
            else:
                print("URL ignorée (pas de point) :", line)
        except:
            pass
    return [array_new_feed, set(name_rss_sender)]

#Vas dans le fichier stopword définit part l'user pour nettoyer les résultat
def stopWordUsual(file = "stopword.txt"):
    stream = open(file, "r")
    arrayStopWord = stream.read()
    return set(arrayStopWord.split("\n"))

#Calcul l'intensité d'un mots à partir de sont nombre d'occurence dans le data set
def calcul_intensity_word(word, word_intensity):
    is_exist = False
    index = 0
    for only_one_word_intensity in range(len(word_intensity)):
        if word_intensity[only_one_word_intensity][0] == word :
            is_exist = True
            index = only_one_word_intensity

    if is_exist == False:
        word_intensity.append([word, 1])
    else :
        contentValue = word_intensity[index][1]
        word_intensity[index][1] = contentValue + 1
    
    return word_intensity

#Exclus tout les mots si leur intensité calculer dans calcul_intensity_word() est inférieur à chiffre définis
def exclude_lowest_intensity_word_by_occurence (word_with_intensity_occurence, limits_intensity = 5):
    intensity_word_with_just_important_occurence = []
    for y in range(len(word_with_intensity_occurence)):
        if word_with_intensity_occurence[y][1] >= limits_intensity:
            intensity_word_with_just_important_occurence.append(word_with_intensity_occurence[y])
    return intensity_word_with_just_important_occurence

#Permet l'affichage des mots trouver dans calcul_intensity_word() est choisi part leur intensité dans exclude_lowest_intensity_word_by_occurence()
def word_insenty_print_important_represent(word_intensity) :
    for only_one_word in range(len(word_intensity)):
        #print(word_intensity[only_one_word])
        pass

#Vas dans le data set trouver tout les mots important (NN) est vas prendre leur voisinage directe avant ou après (n+1) pour avoir des concept les plus précis possible
def find_and_save_context(word, index, content, contextWord, set_stop_word_usual):
    before_realise = False
    if (index-1) >= 0 :
        if  re.match('^(?!nbsp$)[A-Za-z0-9]+$', content[index - 1][0].lower()) :
            if content[index - 1][0].lower() in set_stop_word_usual:
                pass
            else:
                beforeWord = [content[index - 1][0].lower(), word.lower()]
                before_realise = True
    
    if len(content) > (index+1) and before_realise == True :
        if  re.match('^(?!nbsp$)[A-Za-z0-9]+$', content[index + 1][0].lower()) :
            if content[index + 1][0].lower() in set_stop_word_usual:
                pass
            else :
                beforeWord.append(content[index + 1][0].lower())
                contextWord.append(beforeWord)
    elif len(content) > (index+1) and before_realise == False:
        if  re.match('^(?!nbsp$)[A-Za-z0-9]+$', content[index + 1][0].lower()) :
            if content[index + 1][0].lower() in set_stop_word_usual:
                pass
            else :
                contextWord.append([word.lower(), content[index + 1][0].lower()])
    elif before_realise == True:
        contextWord.append(beforeWord)
    return contextWord

#Via matplotlib.pyplot dessine un diagramme de barre des termes selon la limit user, ayant les plus d'occurence dans le data-set permettant d'un coup d'oeil d'un avoir les point important émise part les flux rss
def graph_intensity_word(intensity_word_with_just_important_occurence, limit = 25):
    word_intensity = []
    occurence_intensity = []
    for word_and_occurence in intensity_word_with_just_important_occurence:
        if word_and_occurence[1] >= limit:
            word_intensity.append(word_and_occurence[0])
            occurence_intensity.append(word_and_occurence[1])
    axis.bar(word_intensity, occurence_intensity)
    axis.set_ylabel('Occurrence of a word in articles')
    matplotlib.pyplot.show()


figure_matpolib, axis = matplotlib.pyplot.subplots()

array_stop_word_usual = stopWordUsual()
array_output_parse_rss = parseRss()
intensity_word_with_just_important = []
contex_word_save = []
array_new_feed = array_output_parse_rss[0]
name_rss_organisation_sender = array_output_parse_rss[1]
word_intensity = [["a", 1]]


#Effectu l'ensemble du nettoyage ainsi que de la préparations des données (titre + résumé) fournis part les flux rss pour leur utilisation
for x in range(len(array_new_feed)):
    for i in range(len(array_new_feed[x].entries)):
        #print(arrayNewFeed[x].entries[i]["title"])
        #print(time.strftime("%Y-%m-%d %H:%M:%S", arrayNewFeed[x].entries[i]["published_parsed"]))
        #print(arrayNewFeed[x].entries[i]["summary"])
        #print("\ \ \ \ ")
        rss_tokenize = nlp(array_new_feed[x].entries[i]["title"] + array_new_feed[x].entries[i]["summary"])
        print(type(rss_tokenize))
        tokenize_post = list(nltk.word_tokenize(array_new_feed[x].entries[i]["title"]) + list(nltk.word_tokenize(array_new_feed[x].entries[i]["summary"])))
        tag_tokenize_post = nltk.pos_tag(tokenize_post)
        for j in range(len(tag_tokenize_post)) :
            tag = tag_tokenize_post[j][1]
            word = (tag_tokenize_post[j][0]).lower()
            if tag.startswith("NN") and re.match('^(?!nbsp$)[A-Za-z0-9]+$', word) and len(word) > 1 : 
                lem_word = WordNetLemmatizer().lemmatize(word)
                is_organisation_sender_rss = False
                is_usual_stop_word = False
                if lem_word in name_rss_organisation_sender :
                    is_organisation_sender_rss = True
                if lem_word in array_stop_word_usual:
                    is_usual_stop_word = True
                if is_organisation_sender_rss == False and is_usual_stop_word == False :       
                    word_intensity = calcul_intensity_word(lem_word, word_intensity)
                    contex_word_save = find_and_save_context(lem_word, j, tag_tokenize_post, contex_word_save, array_stop_word_usual)
                                    

#appel des fonctions liès à la categorisation semantique
intensity_word_with_just_important = exclude_lowest_intensity_word_by_occurence(word_intensity)
word_insenty_print_important_represent(intensity_word_with_just_important)
#print(nameRssOrganisationSender)
#print(contexWordSave)

#Affiche de manière ordonnée les mots avec leur contexte via intensity_context()
obj_intensity_context = intensity_context(contex_word_save)
context_number = obj_intensity_context.return_result()
for u in range(len(context_number)):
    if type(context_number[u][2]) == int:
        number = 2
    elif type(context_number[u][3]) == int:
        number = 3 

    # if number == 2 :
    #     if context_number[u][2] > 2 :
    #         print(context_number[u])
    # elif number == 3:
    #     if context_number[u][3] > 0 :
    #         print(context_number[u])

obj_thematic_context = thematic_context(context_number)
semantique_categorie = obj_thematic_context.return_semantic_categorie()
#print(semantique_categorie)

#Affiche le diagramme en barre visant à simplifier la lectures des grand sujet remonter part les flux rss
graph_intensity_word(intensity_word_with_just_important)