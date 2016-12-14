from __future__ import division

def computeForSpamProbability(spam_count, ham_count):
    return spam_count/(spam_count+ham_count)

def computeForHamProbability(spam_count, ham_count):
    return ham_count/(spam_count+ham_count)

def computeForSpamWordProbability(occurence, spam_count):
    return (occurence+1)/(spam_count+2)

def computeForHamWordProbability(occurence, ham_count):
    return (occurence+1)/(ham_count+2)

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
        else:
            multiplicand = word_obj.getHamProbability()

        if isWordIncluded is False:
            multiplicand = 1.0 - multiplicand
            # print 'grr'
        # else:
        #     print 'daan'

        # print email_type
        # print word_obj.getSpamProbability()
        # print word_obj.getHamProbability()
        # print multiplicand
        answer = answer * multiplicand
        # print  'ans'
        # print answer

        # if answer is 0.00:
        #     exit()

    return answer

def computeBayesianProbability(spam_prob, ham_prob, word_spam_prob, word_ham_prob, email_type):

    if email_type is 'spam':
        # print 'word spam'
        # print word_spam_prob
        # print 'spam_prob'
        # print spam_prob
        # print 'word ham'
        # print word_ham_prob
        # print 'ham prob'
        # print ham_prob
        return (word_spam_prob * spam_prob) / (word_spam_prob * spam_prob + word_ham_prob * ham_prob )
    else:
        return (word_ham_prob * ham_prob) / (word_ham_prob * ham_prob + word_spam_prob * spam_prob)
