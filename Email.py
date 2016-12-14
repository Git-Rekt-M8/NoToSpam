class Email:
    def __init__(self):
        self.spamEmail = []
        self.legitEmail = []

    def addSpamEmail(self, email):
        self.spamEmail.append(email)

    def addLegitimateEmail(self, email):
        self.legitEmail.append(email)

    def getSpamEmailList(self):
        return self.spamEmail

    def getLegitEmailList(self):
        return self.legitEmail