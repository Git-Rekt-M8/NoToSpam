from __future__ import division

def computeForSpamProbability(spam_count, ham_count):
    return spam_count/(spam_count+ham_count)

def computeForHamProbability(spam_count, ham_count):
    return ham_count/(spam_count+ham_count)

def computeForSpamWordProbability(occurence, spam_count):
    return occurence/spam_count

def computeForHamWordProbability(occurence, ham_count):
    return occurence/ham_count

def computeProbabilityForListOfWords(attribs_dic, word_list, email_type):
    answer = 1.0
    for word, word_obj in attribs_dic.iteritems():
        isWordIncluded = False

        for word_list_word in word_list:
            if word == word_list_word:
                isWordIncluded = True

        multiplicand = 1.0
        if email_type == 'spam':
            multiplicand = word_obj.getSpamProbability()
            print 'sex'
            print multiplicand
        else:
            multiplicand = word_obj.getHamProbability()

        if isWordIncluded is False:
            multiplicand = 1.0 - multiplicand
        # else:
        #     print 'daan'

        # print 'm: %.2f' % multiplicand
        print 'mul'
        print multiplicand
        answer = answer * multiplicand
        print  'ans'
        print answer
        # print 'a: %.2f' % answer

        # if answer is 0.00:
        #     exit()

    return answer

def computeBayesianProbability(spam_prob, ham_prob, word_spam_prob, word_ham_prob, email_type):

    if email_type is 'spam':
        return (word_spam_prob * spam_prob) / (word_spam_prob * spam_prob + word_ham_prob * ham_prob )
    else:
        return (word_ham_prob * ham_prob) / (word_ham_prob * ham_prob + word_spam_prob * spam_prob)
