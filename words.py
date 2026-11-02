


#This file has 1000 common words
with open("commonwords.txt") as f:
    common_words = []
    for line in f:
        common_words.append(line.strip())

common_words = set(common_words)

def get_common_words():
    return common_words

