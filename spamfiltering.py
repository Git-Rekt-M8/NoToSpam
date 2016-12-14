import os
import re
import UtilsForBae as bae
import math

import operator
import itertools

from decimal import Decimal
from random import randint

from Word import Word

words_dic = {}
SPAM_PROBABILITY = 0
HAM_PROBABILITY = 0
word_list = ['hi']
attribs_dic = {}
spam_count = 0.0
ham_count = 0.0
email_dir = 'emails/bare'
part_folder = '/part'

# Load Data
def init(test_folder_index):
    global spam_count
    global ham_count
    global SPAM_PROBABILITY
    global  HAM_PROBABILITY

    # 10-fold cross validation means repeat 10 times: divide data into 10, use 9 for training, 1 for testing
    #test_folder_index = 1 # randint(1, 10)
    print test_folder_index

    test_folder = 1
    print test_folder


    for num in range(1, 11):
        if num != test_folder_index:
            part_num = num
            part_folder = '/part' + str(part_num)
            print part_folder
            for filename in os.listdir(email_dir + part_folder):
                email_type = 'ham'
                if 'sp' in filename:
                    email_type = 'spam'
                    spam_count += 1
                else:
                    ham_count += 1
                email_file = open(email_dir + part_folder + "/" + filename, "r")
                content = email_file.read()


                train(content, email_type)
                #print email_file
    # DA PRIORS BITCHES
    SPAM_PROBABILITY = bae.computeForSpamProbability(spam_count, ham_count)
    HAM_PROBABILITY = bae.computeForHamProbability(spam_count, ham_count)

    for word, word_obj in words_dic.iteritems():
        words_dic[word].setSpamProbability(bae.computeForSpamWordProbability(word_obj.getSpamOccur(), spam_count))
        words_dic[word].setHamProbability(bae.computeForHamWordProbability(word_obj.getHamOccur(), ham_count))
        #print "Value : %d" % words_dic['subject'].getSpamOccur()

    compute()
    getTopAttribs(50)

def train(content, email_type):
    # print 'choo choo motherfucker'
    allwords_array = getWordsFromEmail(content)
    # print(allwords_array)
    words_array = set(allwords_array) #remove duplicates
    for word in words_array:
        word_obj = words_dic.get(word, None)
        if word_obj is None:
            word_obj = Word()
            word_obj.setContent(word)

        if email_type == 'spam':
            word_obj.addToSpamOccur(1)
        else:
            word_obj.addToHamOccur(1)
        words_dic[word] = word_obj


def compute():
    total = ham_count + spam_count
    for key, value in words_dic.iteritems():
        spam_occur = value.getSpamOccur()
        spam_notoccur = spam_count - spam_occur
        ham_occur = value.getHamOccur()
        ham_notoccur = total - value.getHamOccur()
        # print Decimal((total * ham_occur) / ((spam_occur + ham_occur) * (ham_occur + ham_notoccur)))
        try:
            mutual_info = (spam_occur / total) * math.log((total * spam_occur) / ((spam_occur + ham_occur) * (spam_occur + spam_notoccur)))
        except:
            mutual_info = 0.0

        try:
            mutual_info += (spam_notoccur / total) * math.log((total * spam_notoccur) / ((spam_notoccur + ham_notoccur) * (spam_occur + spam_notoccur)))
        except:
            mutual_info += 0.0

        try:
            mutual_info += (ham_occur / total) * math.log((total * ham_occur) / ((spam_occur + ham_occur) * (ham_occur + ham_notoccur)))
        except:
            mutual_info += 0.0

        try:
            mutual_info += (ham_notoccur / total) * math.log((total * ham_notoccur) / ((spam_notoccur + ham_notoccur) * (ham_occur + ham_notoccur)))
        except:
            mutual_info += 0.0
        # print mutual_info
        words_dic[key].setMutualInfo(mutual_info)


def getTopAttribs(n):
    sorted_dic = sorted(words_dic.values(), key=lambda word: word.mutualInfo, reverse=True)
    top_n = sorted_dic[:n]
    for word in top_n:
        attribs_dic[word.getContent()] = word
        print str(word.getContent()) + ' = ' + str(word.getMutualInfo())
    return attribs_dic

def getWordsFromEmail(content):
    #content = re.sub(r'[^\w\s]', '', content)
    content = re.sub('[^a-zA-Z]+', ' ', content)
    content = content.lower()
    return content.split()

def testEmail(test_email):
    email_file = open('emails/bare' + "/part1" + "/" + test_email, "r")
    content = email_file.read()
    word_list = getWordsFromEmail(content)
    word_list = set(word_list)  # remove duplicates

    # get top n
    # attribs_dic = bae.getTopAttribs(50)
    #attribs_dic = ['hi']
    word_spam_prob = bae.computeProbabilityForListOfWords(attribs_dic, word_list, "spam")
    word_ham_prob = bae.computeProbabilityForListOfWords(attribs_dic, word_list, "ham")

    print 'pakyu ol'
    print word_spam_prob
    print word_ham_prob

    email_type = "spam"

    baye_probability = bae.computeBayesianProbability(SPAM_PROBABILITY, HAM_PROBABILITY, word_spam_prob, word_ham_prob,
                                                      email_type)

    print 'answer??'
    print baye_probability
    #get bayesian

# MAIN
test_folder_index = 1
init(test_folder_index)

for filename in os.listdir(email_dir + part_folder + str(test_folder_index)):
    testEmail(filename)


#print "Value : %f" %  words_dic['hello'].getHamProbability()

#print words_dic['Subject'].getSpamOccur()
#print "Value : %d" %  words_dic['subject'].getSpamOccur()
#print spam_count



