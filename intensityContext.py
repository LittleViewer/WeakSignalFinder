
class intensity_context:
    
    #init sert ici de pipeline d'execution à la classe intensity_context
    def __init__(self, context):
        context_number = [["a", "b", "c", 1]]
        self.context_cache = {}
        for sentence_tales in range(len(context)):
            key = tuple(context[sentence_tales])
            if key in self.context_cache:
                idx = self.context_cache[key]
                context_number[idx][-1] += 1
            else:
                context_number = self.add_sentence(context[sentence_tales], context_number)
                self.context_cache[key] = len(context_number) - 1

        self.context_with_intensity = context_number
        self.return_result()
            
    #compare si un context est déjà présent dans l'ensemble des context déjà présent
    def compare_one_sentence(self, sentence, context_tales):
        is_exist = False
        for context_tales_count in range(len(context_tales)):
            number_section = len(context_tales[context_tales_count])
            if number_section == 3 :
                if [context_tales[context_tales_count][0],context_tales[context_tales_count][1]] == sentence:
                    is_exist = [True, context_tales_count]
                elif [context_tales[context_tales_count][0],context_tales[context_tales_count][1],context_tales[context_tales_count][2]] == sentence:
                    is_exist = [True, context_tales]
        return is_exist
    
    #Si la categorie n'existe pas selon compare_one_sentence() elle est ajouter à l'ensemble avec un index (compteur d'occurence) définis à 1
    def add_sentence(self, sentence, context_tales):
        sentence.append(1)
        context_tales.append(sentence)
        return context_tales
    
    #Si la categorie existe selon compare_one_sentence() on vient modifier l'index pour que se dernier puissent refleter la nouvelle occurence (1 mis a 2)
    def sentence_exist(self, context_tales, is_exist):
        numbser_section = len(context_tales[is_exist[1]])
        if numbser_section == 3:
            context_tales[is_exist[1]][2] = context_tales[is_exist[1]][2] + 1
        elif numbser_section == 4:
            context_tales[is_exist[1]][3] = context_tales[is_exist[1]][3] + 1
        return context_tales
    
    #Retourne le résultat de tout les contexte trouver de deux (before-central_word/central-word-after) ou triplet (before-word_central-before)
    def return_result(self ):
        return self.context_with_intensity
    
class thematic_context :

    #init sert ici de pipeline d'execution à la classe thematic_context
    def __init__(self, context_with_intensity):
        central_semantic_word = self.find_word_context_by_semantic_for_categorized(context_with_intensity)
        dictionnary_for_semantic_categorized = self.create_dictionnary_for_semantic_categorized(central_semantic_word)
        dictionnary_semantic_central_word_with_context = self.semantic_categorie(context_with_intensity, dictionnary_for_semantic_categorized, central_semantic_word)
        self.semantic_categorie = self.cleaner_semantic_categorie(central_semantic_word, dictionnary_semantic_central_word_with_context)

    #Permet de trouver tout les mots dit central se trouvent comment mots pivot entre after et before dans intensity_context
    def find_word_context_by_semantic_for_categorized(self, context_with_intensity):
        central_semantic_word = []
        for word_present_in_context in context_with_intensity:
                section_context = len(word_present_in_context)
                central_semantic_word.append(word_present_in_context[0])
                central_semantic_word.append(word_present_in_context[1])
                if section_context == 4:
                    central_semantic_word.append(word_present_in_context[2])
        central_semantic_word = set(central_semantic_word)
        return list(central_semantic_word)
    
    def create_dictionnary_for_semantic_categorized(self, semantic_central_word):
        dictionnary = {}
        for word_central in semantic_central_word:
            dictionnary[word_central] = {"Before" : [], "After" : []}
        return dictionnary

    #Permet de récupéré tout le voisinage avant ou après des mots centraux définit part find_word_context_by_semantic_engine() afin d'obtenir des catégorie sémantique qui regroupent tout les mot n-1 ou n+1 du central word afin que l'utilisateur puissent se faire des idées des discussion qu'il y a autour de différent termes centraux (émergent ou majeur) soulever part les flux rss
    def semantic_categorie(self, context_with_intensity, dictionnary_semantic_central_word, central_semantic_word):
        for only_one_word_central_by_context in context_with_intensity:
            #print(only_one_word_central_by_context)
            if len(only_one_word_central_by_context) == 4:
                tmp_dict_section = dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["Before"]
                tmp_dict_section.append(only_one_word_central_by_context[0])
                dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["Before"] = list(set(tmp_dict_section))

                tmp_dict_section = dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["After"]
                tmp_dict_section.append(only_one_word_central_by_context[2])
                dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["After"] = list(set(tmp_dict_section))

            elif len(only_one_word_central_by_context) == 3 :
                    wordBefore = only_one_word_central_by_context[0]
                    wordAfter = only_one_word_central_by_context[1]
                    if wordAfter in central_semantic_word:
                        tmp_dict_section = dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["Before"]
                        tmp_dict_section.append(only_one_word_central_by_context[0])
                        dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["Before"] = list(set(tmp_dict_section))
                    if wordBefore in central_semantic_word:
                        tmp_dict_section = dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["After"]
                        tmp_dict_section.append(only_one_word_central_by_context[1])
                        dictionnary_semantic_central_word[only_one_word_central_by_context[1]]["After"] = list(set(tmp_dict_section))

        return dictionnary_semantic_central_word

        
    #Permet de nettoyer le résultat de semantic_categorie() des catégorie sémantique des central_word qui n'aurait pas de mots important (pas stop word et NN) dans le voisingae n-1 ou n+1
    def cleaner_semantic_categorie(self, word_central, dictionnary_semantic_central_word, limit = 4):
        for only_one_word_central in word_central:
            if (len(dictionnary_semantic_central_word[only_one_word_central]["Before"]) + len(dictionnary_semantic_central_word[only_one_word_central]["After"])) < limit:
                del dictionnary_semantic_central_word[only_one_word_central]
        return dictionnary_semantic_central_word

    #Permet de renvoyer le résultat de l'ensemble du pipeline
    def return_semantic_categorie(self):
        return self.semantic_categorie
