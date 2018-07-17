# -*- coding: utf-8 -*-
"""
@author: Casey
"""

import sys
import json
import csv
import re
import string


def hw():
    print('Hello, world!')


def lines(fp):
    print(str(len(fp.readlines())))


def main():
    sent_file = open(sys.argv[1])
    tweet_file = open(sys.argv[2])
    hw()
    lines(sent_file)
    lines(tweet_file)

    # Load sentiment file and tweets into lists

    sentiments = {}
    tweets = []

    with open(sys.argv[1]) as f:
        for line in csv.reader(f, delimiter="\t"):
            sentiments[line[0]] = int(line[1])

    with open(sys.argv[2]) as f:
        for line in f:
            tweets.append(json.loads(line))

    # Set regex for removing punctuation
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    # Cycle through tweets, getting overall sentiment and determining word
    # sentiments

    word_sent = {}

    for tweet in tweets:

        if "text" in tweet:
            # Restrict to English, as any non-english words will not be
            # detected during tweet sentiment calculation, which influences
            # in word sentiment scores.
            if tweet["lang"] == "en":
                this_sent = 0

                text = tweet["text"]
                text = regex.sub("", text)
                text = text.lower()

                for word in text.split(" "):
                    if word in sentiments:
                        this_sent += sentiments[word]

                for word in text.split(" "):
                    # Add word to word_sent dictionary if not already present
                    # [0] is positive counter, [1] is negative counter

                    # Set to 1/1 so neutral sentiment is 1; posive > 1
                    # negative < 1in final calculation os sentiment scores
                    if word not in sentiments:
                        if word not in word_sent:
                            word_sent[word] = [1, 1]
                        # Adjust word sentiment score:
                        if word in word_sent:
                            if this_sent > 0:
                                word_sent[word][0] += 1
                            elif this_sent < 0:
                                word_sent[word][1] += 1

    # Calculate word sentiment scores
    for word in word_sent:
        word_sent[word] = word_sent[word][0]/word_sent[word][1]

    # Write to file for inspection
#    with open("term_sentiment.txt", "w+") as f:
#        for word in word_sent:
#            f.write("%s    %f\n"%(word, word_sent[word]))

    # Print word sentiments, each element on a new line
    # NOTE: Windows nor Git Bash support emojis, thus running on Windows
    # results in UnicodeEncodeError
    for word in word_sent:
        try:
            print(word, word_sent[word])
        except UnicodeEncodeError:
            print("UnicodeEncodeError: Character is either emoji or misc ",
                  "symbol/pictograph and unsupported by Windows/OS/prompt. ",
                  "Will not print word sentiment.")


if __name__ == '__main__':
    main()
