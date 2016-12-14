class Word:
    def __init__(self):
        self.spamOccurence = 0
        self.hamOccurence = 0


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
