import os
from random import randint

from Email import Email

folderList = []

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
                content = email_file.readlines()
                train(content, email_type)
                #print email_file


def train(content, email_type):
    print 'choo choo motherfucker'
    email = Email()

    if email_type == 'sp':
        email.addSpamEmail(content)
    else:
        email.addLegitimateEmail(content)

    folderList.append(email)


load_files()
print 'hi'



