
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