class Word:
    def __init__(self):
        self.content = ''
        self.spamOccurence = 0.0
        self.hamOccurence = 0.0
        self.mutualInfo = 0.0


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

