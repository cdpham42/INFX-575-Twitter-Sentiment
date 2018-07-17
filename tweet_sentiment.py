# -*- coding: utf-8 -*-
"""
@author: Casey
"""

import sys
import json
import csv
import string
import re


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

    # Verify length
    print(len(sentiments))
    print(len(tweets))

    tweet_sent = []

    # Set regex for removing punctuation
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    # Go through each tweet, determine if tweet has text, clean, and determine
    # sentiment
    for tweet in tweets:

        if "text" in tweet:
            this_sent = 0

            text = tweet["text"]
            text = regex.sub("", text)
            text = text.lower()

            for word in text.split(" "):
                if word in sentiments:
                    this_sent += sentiments[word]

            tweet_sent.append(this_sent)

        else:
            tweet_sent.append(0)
            continue

    # Print tweet sentiments, each element on a new line
    for s in tweet_sent:
        print(s)


if __name__ == '__main__':
    main()
