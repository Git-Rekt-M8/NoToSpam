from __future__ import division
import os
import re
import UtilsForBaye as baye
import math
import csv

import operator
import itertools

from decimal import Decimal
from random import randint

from Word import Word


threshold_lambda = 1.0
num_of_top_attributes = 50
epsilon = 1.0

words_dic_list = []
SPAM_PROBABILITY = [0.0 for k in range(10)]
HAM_PROBABILITY = [0.0 for k in range(10)]
attribs_dic = {}
spam_count = 0.0
ham_count = 0.0
email_dir = 'emails/lemm'
part_folder = '/part'

# tests
spam_fp_count = 0 #ham na spam / spam na mali
spam_fn_count = 0 #spam na ham / ham na spam dapat
spam_correct_count = 0 #abay pro spam checking
ham_correct_count = 0
spam_true_count = 0 #kung ilan talaga, based on filename
ham_true_count = 0

#analysis
spam_recall = []
spam_precision = []
weighted_accuracy = []
baseline_weighted_accuracy = []
tcr = []

#csv
csv_data_list = []



# Load Data
def init(test_folder_index):
    global spam_count
    global ham_count
    global SPAM_PROBABILITY
    global HAM_PROBABILITY

    words_dic_index = test_folder_index -1

    # 10-fold cross validation means repeat 10 times: divide data into 10, use 9 for training, 1 for testing

    words_dic_list[words_dic_index].clear()
    attribs_dic.clear()
    spam_count = 0.0
    ham_count = 0.0

    for num in range(1, 11):
        if num != test_folder_index:
            part_num = num
            part_folder = '/part' + str(part_num)

            for filename in os.listdir(email_dir + part_folder):
                email_type = 'ham'
                if 'sp' in filename:
                    email_type = 'spam'
                    spam_count += 1
                else:
                    ham_count += 1
                email_file = open(email_dir + part_folder + "/" + filename, "r")
                content = email_file.read()

                train(content, email_type, words_dic_index)
    # PRIORS
    SPAM_PROBABILITY[words_dic_index] = baye.computeForSpamProbability(spam_count, ham_count)
    HAM_PROBABILITY[words_dic_index] = baye.computeForHamProbability(spam_count, ham_count)

    for word, word_obj in words_dic_list[words_dic_index].iteritems():
        words_dic_list[words_dic_index].get(word).setSpamProbability(
            baye.computeForSpamWordProbability(word_obj.getSpamOccur(), spam_count, epsilon))
        words_dic_list[words_dic_index].get(word).setHamProbability(
            baye.computeForHamWordProbability(word_obj.getHamOccur(), ham_count, epsilon))

    computeMI(words_dic_index)

def init_per_test_folder():
    global spam_fp_count  # ham na spam / spam na mali
    global spam_fn_count  # spam na ham / ham na spam dapat
    global spam_correct_count  # abay pro spam checking
    global ham_correct_count
    global spam_true_count  # kung ilan talaga, based on filename
    global ham_true_count

    spam_fp_count = 0  # ham na spam / spam na mali
    spam_fn_count = 0  # spam na ham / ham na spam dapat
    spam_correct_count = 0  # abay pro spam checking
    ham_correct_count = 0
    spam_true_count = 0  # kung ilan talaga, based on filename
    ham_true_count = 0

def train(content, email_type, words_dic_index):
    allwords_array = getWordsFromEmail(content)
    words_array = set(allwords_array) #remove duplicates
    for word in words_array:
        word_obj = words_dic_list[words_dic_index].get(word, None)
        if word_obj is None:
            word_obj = Word()
            word_obj.setContent(word)

        if email_type == 'spam':
            word_obj.addToSpamOccur(1)
        else:
            word_obj.addToHamOccur(1)
        words_dic_list[words_dic_index][word] = word_obj


def computeMI(words_dic_index):
    total = ham_count + spam_count
    for key, value in words_dic_list[words_dic_index].iteritems():
        spam_occur = value.getSpamOccur()
        spam_notoccur = spam_count - spam_occur
        ham_occur = value.getHamOccur()
        ham_notoccur = total - value.getHamOccur()
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
        words_dic_list[words_dic_index][key].setMutualInfo(mutual_info)


def getTopAttribs(n, words_dic_index):
    values_dic = words_dic_list[words_dic_index]
    sorted_dic = sorted(values_dic.values(), key=lambda word: word.mutualInfo, reverse=True)
    top_n = sorted_dic[:n]
    for word in top_n:
        attribs_dic[word.getContent()] = word
    return attribs_dic

def getWordsFromEmail(content):
    content = re.sub('[^a-zA-Z]+', ' ', content)
    content = content.lower()
    return content.split()

def checkSpamHam(threshold, prob_spam):
    t = threshold / (threshold + 1)
    if (prob_spam > math.log(t)):
        return 'spam'
    return 'ham'

def testEmail(test_email, words_dic_index):

    email_file = open(test_email, "r")
    content = email_file.read()
    word_list = getWordsFromEmail(content)
    word_list = set(word_list)  # remove duplicates

    word_spam_prob = baye.computeProbabilityForListOfWords(attribs_dic, word_list, "spam")
    word_ham_prob = baye.computeProbabilityForListOfWords(attribs_dic, word_list, "ham")

    email_type = "spam"

    baye_probability = baye.computeBayesianProbability(SPAM_PROBABILITY[words_dic_index], HAM_PROBABILITY[words_dic_index], word_spam_prob, word_ham_prob,
                                                       email_type)

    return checkSpamHam(threshold_lambda, baye_probability)


# MAIN
filter_types = ['bare','lemm','lemm_stop','stop']
lambda_values = [1,9,999]
max_num_of_top_attributes = 700

#initialize dictionary
words_dic_list = [{} for k in range(10)]

#for each filter type
for filter_config in filter_types:
    print 'TRAINING FILTER FOR: ' + filter_config
    for test_folder_index in range(1, 11):
        init(test_folder_index)
    #for each max attribute
    num_of_top_attributes = 50 # reinitialize num of attributes
    while num_of_top_attributes <= max_num_of_top_attributes:
        #for each lambda
        for lambda_current in lambda_values:
            threshold_lambda = lambda_current
            email_dir = 'emails/' + filter_config
            print 'TESTING'
            print 'Filter Configuration: %s' % filter_config.capitalize()
            print 'Number of Attributes: %d' % num_of_top_attributes
            print 'Lambda Value: %d' % lambda_current

            spam_recall = []
            spam_precision = []
            weighted_accuracy = []
            baseline_weighted_accuracy = []
            tcr = []
            # for each test folder
            for num in range(1, 11):
                init_per_test_folder()
                getTopAttribs(num_of_top_attributes, num-1)
                email_count = 0
                # for each email
                for filename in os.listdir(email_dir + part_folder + str(num)):
                    # check if spam or ham indication
                    if 'sp' in filename:
                        test_email_type = 'spam'
                        spam_true_count += 1
                    else:
                        test_email_type = 'ham'
                        ham_true_count += 1

                    bayesian_result = testEmail(email_dir + part_folder + str(num) + "/" + filename, num-1)

                    # update results for analysis
                    if bayesian_result == 'spam' and test_email_type == 'spam':
                        spam_correct_count += 1
                    elif bayesian_result == 'ham' and test_email_type == 'ham':
                        ham_correct_count += 1
                    elif bayesian_result == 'spam' and test_email_type == 'ham':
                        spam_fp_count += 1
                    elif bayesian_result == 'ham' and test_email_type == 'spam':
                        spam_fn_count += 1

                spam_recall.append(spam_correct_count / (spam_correct_count + spam_fn_count))
                spam_precision.append(spam_correct_count / (spam_correct_count + spam_fp_count))
                weighted_accuracy.append((threshold_lambda * ham_correct_count + spam_correct_count) / (threshold_lambda * ham_true_count + spam_true_count))
                baseline_weighted_accuracy.append((threshold_lambda * ham_true_count) / (threshold_lambda * ham_true_count + spam_true_count))
                tcr.append(spam_true_count / (threshold_lambda * spam_fp_count + spam_fn_count))

            # PLACE IN CSV FILE
            data = [filter_config, lambda_current, num_of_top_attributes]

            print 'RESULTS'
            print_value = (sum(spam_recall) / float(len(spam_recall))) * 100
            data.append(print_value)
            print 'Spam Recall: %.2f %%' % print_value
            print_value = (sum(spam_precision) / float(len(spam_precision))) * 100
            data.append(print_value)
            print 'Spam Precision: %.2f %%' % print_value
            print_value = (sum(weighted_accuracy) / len(weighted_accuracy)) * 100
            data.append(print_value)
            print 'Weighted Accuracy: %.2f %%' % print_value
            print_value = (sum(baseline_weighted_accuracy) / len(baseline_weighted_accuracy)) * 100
            data.append(print_value)
            print 'Baseline Weighted Accuaracy: %.2f %%' % print_value
            print_value = (sum(tcr) / len(tcr))
            data.append(print_value)
            print 'TCR: %.2f \n' % print_value

            csv_data_list.append(data)

        num_of_top_attributes += 50 # step of 50

with open('results.csv', 'wb') as fp:
    a = csv.writer(fp, delimiter=',')
    a.writerows(csv_data_list)
