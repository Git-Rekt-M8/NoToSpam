import os
from random import randint


# Load Data
def load_files():
    email_dir = 'emails/bare'
    # 10-fold cross validation means repeat 10 times: divide data into 10, use 9 for training, 1 for testing
    test_folder = randint(1, 10)
    print test_folder
    for num in range(1, 11):
        if num != test_folder:
            part_num = num
            part_folder = '/part' + str(part_num)
            print part_folder
            for filename in os.listdir(email_dir + part_folder):
                type = 'ham'
                if 'sp' in filename:
                    type = 'spam'
                email_file = open(email_dir + part_folder + "/" + filename, "r")
                content = email_file.readlines()
                train(content, type)
                #print email_file

def train(content. type):
    print 'choo choo motherfucker'

load_files()
print 'hi'



