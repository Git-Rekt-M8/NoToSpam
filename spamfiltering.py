import os
import re
import UtilsForBae as bae
from random import randint

from Word import Word

words_dic = {}
SPAM_PROBABILITY = 0
HAM_PROBABILITY = 0


# Load Data
def load_files():
    email_dir = 'emails/bare'
    # 10-fold cross validation means repeat 10 times: divide data into 10, use 9 for training, 1 for testing
    test_folder = 1 #randint(1, 10)
    print test_folder

    for num in range(1, 11):
        if num != test_folder:
            part_num = num
            part_folder = '/part' + str(part_num)
            print part_folder
            for filename in os.listdir(email_dir + part_folder):
                email_type = 'ham'
                if 'sp' in filename:
                    email_type = 'spam'
                email_file = open(email_dir + part_folder + "/" + filename, "r")
                content = email_file.read()
                train(content, email_type)
                #print email_file


def train(content, email_type):
    #print 'choo choo motherfucker'
    allwords_array = getWordsFromEmail(content)
    #print(allwords_array)
    words_array = set(allwords_array) #remove duplicates
    for word in words_array:
        word_obj = words_dic.get(word, None)
        if word_obj is None:
            word_obj = Word()

        if email_type == 'spam':
            word_obj.addToSpamOccur(1)
        else:
            word_obj.addToHamOccur(1)
        words_dic[word] = word_obj


def getWordsFromEmail(content):
    content = re.sub(r'[^\w\s]', '', content)
    content = content.lower()
    return content.split()

# MAIN
load_files()
#print words_dic['Subject'].getSpamOccur()
print "Value : %d" %  words_dic['subject'].getSpamOccur()



