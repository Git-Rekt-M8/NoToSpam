class Word:
    def __init__(self):
        self.spamOccurence = 0
        self.hamOccurence = 0
        self.spamProbability = 0.0
        self.hamProbability = 0.0
        self.content = ''
        self.mutualInfo = 0.0

    def getSpamProbability(self):
        return self.spamProbability

    def setSpamProbability(self, n):
        self.spamProbability = n

    def getHamProbability(self):
        return self.hamProbability

    def setHamProbability(self, n):
        self.hamProbability = n

    def addToSpamOccur(self, n):
        self.spamOccurence +=n

    def addToHamOccur(self, n):
        self.hamOccurence +=n

    def getSpamOccur(self):
        return self.spamOccurence

    def getHamOccur(self):
        return self.hamOccurence

    def setSpamOccur(self, n):
        self.spamOccurence = n

    def setHamOccur(self, n):
        self.hamOccurence = n

    def getMutualInfo(self):
        return self.mutualInfo

    def setMutualInfo(self, n):
        self.mutualInfo = n

    def getContent(self):
        return self.content

    def setContent(self, n):
        self.content = n

