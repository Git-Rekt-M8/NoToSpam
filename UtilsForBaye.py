from __future__ import division
import math
import numpy

def computeForSpamProbability(spam_count, ham_count):
    return spam_count/(spam_count+ham_count)

def computeForHamProbability(spam_count, ham_count):
    return ham_count/(spam_count+ham_count)

def computeForSpamWordProbability(occurence, spam_count, epsilon):
    return (occurence+1*epsilon)/(spam_count+2*epsilon)

def computeForHamWordProbability(occurence, ham_count, epsilon):
    return (occurence+1*epsilon)/(ham_count+2*epsilon)

def computeProbabilityForListOfWords(attribs_dic, word_list, email_type):
    answer = 0.0
    for word, word_obj in attribs_dic.iteritems():
        isWordIncluded = False

        for word_list_word in word_list:
            if word == word_list_word:
                isWordIncluded = True

        multiplicand = 1.0
        if email_type == 'spam':
            multiplicand = word_obj.getSpamProbability()
        else:
            multiplicand = word_obj.getHamProbability()

        if isWordIncluded is False:
            multiplicand = 1.0 - multiplicand
        answer += math.log(multiplicand)

    return answer

def computeBayesianProbability(spam_prob, ham_prob, word_spam_prob, word_ham_prob, email_type):

    if email_type is 'spam':
        return word_spam_prob + math.log(spam_prob) - numpy.logaddexp(word_spam_prob + math.log(spam_prob), word_ham_prob + math.log(ham_prob) )
    else:
        return (word_ham_prob * ham_prob) / (word_ham_prob * ham_prob + word_spam_prob * spam_prob)

