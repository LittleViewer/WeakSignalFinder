
class intensityContext:
    
    def __init__(self, context):
        contextNumber = [["a", "b", "c", 1]]

        for sentenceCount in range(len(context)):
            isExist = self.compareOneSentence(context[sentenceCount], contextNumber)
            if isExist == False:
               contextNumber = self.addSentence(context[sentenceCount],contextNumber)
            elif isExist[0] == True:
                contextNumber = self.sentenceExist(contextNumber, isExist)
        self.contextNumber = contextNumber
        self.returnValue()
            

    def compareOneSentence(self, sentence, contextNumber):
        isExist = False
        for contextCount in range(len(contextNumber)):
            numberSection = len(contextNumber[contextCount])
            if numberSection == 3 :
                if [contextNumber[contextCount][0],contextNumber[contextCount][1]] == sentence:
                    isExist = [True, contextCount]
                elif [contextNumber[contextCount][0],contextNumber[contextCount][1],contextNumber[contextCount][2]] == sentence:
                    isExist = [True, contextCount]
        return isExist

    def addSentence(self, sentence, contextNumber):
        sentence.append(1)
        contextNumber.append(sentence)
        return contextNumber
    
    def sentenceExist(self, contextNumber, isExist):
        numberSection = len(contextNumber[isExist[1]])
        if numberSection == 3:
            contextNumber[isExist[1]][2] = contextNumber[isExist[1]][2] + 1
        elif numberSection == 4:
            contextNumber[isExist[1]][3] = contextNumber[isExist[1]][3] + 1
        return contextNumber
    
    def returnValue(self ):
        return self.contextNumber
    
class thematicContext :

    def __init__(self, numberContext):
        centralThematicWord = self.findWordThematic(numberContext)
        semantiqueCategorie = self.semantiqueCategorie(numberContext, centralThematicWord)
        print(self.cleanerSemantiqueCategorie(semantiqueCategorie))

    def findWordThematic(self, numberContext):
        centralThematicWord = []
        for wordPresentInContext in numberContext:
                sectionContext = len(wordPresentInContext)
                centralThematicWord.append(wordPresentInContext[0])
                centralThematicWord.append(wordPresentInContext[1])
                if sectionContext == 4:
                    centralThematicWord.append(wordPresentInContext[2])
        centralThematicWord = set(centralThematicWord)
        return list(centralThematicWord)
    
    def semantiqueCategorie(self, numberContext, centralThematicWord):
        familyLinkWord = []
        for wordCentral in centralThematicWord:
            familyLinkWord.append(wordCentral)
            familyLinkWord.append(["After",[],"Before",[]])
            for wordContext in numberContext:
                for i in range(len(wordContext)):
                    if wordCentral == wordContext[i]:
                        for x in range(len(familyLinkWord)):
                                if familyLinkWord[x] == wordCentral:
                                    for z in range(len(familyLinkWord[x+1])):
                                        if i == 0 and range(len(familyLinkWord[x+1])) == 3:
                                            if familyLinkWord[x+1][z] == "After":
                                                familyLinkWord[x+1][z+1].append(wordContext[i+1])
                                                familyLinkWord[x+1][z+1] = list(set(familyLinkWord[x+1][z+1]))
                                        if i == 1:
                                            if familyLinkWord[x+1][z] == "Before":
                                                familyLinkWord[x+1][z+1].append(wordContext[i-1])
                                                familyLinkWord[x+1][z+1] = list(set(familyLinkWord[x+1][z+1]))
                                        if i == 0 and len(familyLinkWord[x+1]) == 4 :
                                            if familyLinkWord[x+1][z] == "After":
                                                familyLinkWord[x+1][z+1].append(wordContext[i+1])
                                                familyLinkWord[x+1][z+1] = list(set(familyLinkWord[x+1][z+1]))
        return familyLinkWord

    def cleanerSemantiqueCategorie(self, semantiqueCategorie):
        for x in range(len(semantiqueCategorie)):
                if len(semantiqueCategorie[x]) > 3:
                    if semantiqueCategorie[x][1] == "" and semantiqueCategorie[x][3] == "":
                        semantiqueCategorie.pop(x-1)
                        semantiqueCategorie.pop(x)
        return semantiqueCategorie
