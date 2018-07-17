# -*- coding: utf-8 -*-
"""
@author: Casey
"""

import sys
import json
import re
import string


def main():

    tweets = []

    with open(sys.argv[1]) as f:
        for line in f:
            tweets.append(json.loads(line))

    # Set regex for removing punctuation
    regex = re.compile('[%s]' % re.escape(string.punctuation))

    word_freq = {}

    for tweet in tweets:

        if "text" in tweet:
            # Restrict to English, as any non-english words will not be
            # detected during tweet sentiment calculation, which influences
            # in word sentiment scores.
            if tweet["lang"] == "en":
                text = tweet["text"]
                text = regex.sub("", text)
                text = text.lower()

                for word in text.split(" "):
                    if word in word_freq:
                        word_freq[word] += 1
                    elif word not in word_freq:
                        word_freq[word] = 1

    for word in word_freq:
        try:
            print(word, word_freq[word])
        except UnicodeEncodeError:
            print("UnicodeEncodeError: Character is either emoji or misc ",
                  "symbol/pictograph and unsupported by Windows/OS/prompt. ",
                  "Will not print word frequency.")


if __name__ == '__main__':
    main()
