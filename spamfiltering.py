import os
import re
import UtilsForBae as bae
from random import randint

from Word import Word

words_dic = {}
SPAM_PROBABILITY = 0
HAM_PROBABILITY = 0
spam_count = 0
ham_count = 0
word_list = ['hi']

# Load Data
def init(test_folder_index):
    global spam_count
    global ham_count
    global SPAM_PROBABILITY
    global  HAM_PROBABILITY

    email_dir = 'emails/bare'
    # 10-fold cross validation means repeat 10 times: divide data into 10, use 9 for training, 1 for testing
    #test_folder_index = 1 # randint(1, 10)
    print test_folder_index

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

def train(content, email_type):
    # print 'choo choo motherfucker'
    allwords_array = getWordsFromEmail(content)
    # print(allwords_array)
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

def testEmail(test_email):
    email_file = open('emails/bare' + "/part1" + "/" + test_email, "r")
    content = email_file.read()
    word_list = getWordsFromEmail(content)

    # get top n
    # attribs_dic = bae.getTopAttribs(50)
    attribs_dic = ['hi']
    word_spam_prob = bae.computeProbabilityForListOfWords(attribs_dic, word_list, "spam")
    word_ham_prob = bae.computeProbabilityForListOfWords(attribs_dic, word_list, "ham")

    print 'pakyu ol'
    print word_spam_prob
    print word_ham_prob

    email_type = "spam"

    baye_probability = bae.computeBayesianProbability(SPAM_PROBABILITY, HAM_PROBABILITY, word_spam_prob, word_ham_prob,
                                                      email_type)

    print baye_probability
    #get bayesian



# MAIN
test_folder_index = 1;
init(test_folder_index)

testEmail("3-1msg1.txt")


#print "Value : %f" %  words_dic['hello'].getHamProbability()
#print words_dic['Subject'].getSpamOccur()
#print "Value : %d" %  words_dic['subject'].getSpamOccur()
#print spam_count
print SPAM_PROBABILITY
print HAM_PROBABILITY



