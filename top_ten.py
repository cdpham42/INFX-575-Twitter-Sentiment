# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 16:25:10 2018

@author: Casey
"""

import sys
import json
import pandas as pd


def main():

    # Load and tweets into list
    tweets = []

    with open(sys.argv[1]) as f:
        for line in f:
            tweets.append(json.loads(line))

    hashtags = {}

    for tweet in tweets:
        if "entities" in tweet:
            for hashtag in tweet["entities"]["hashtags"]:
                if hashtag["text"] in hashtags:
                    hashtags[hashtag["text"]] += 1
                elif hashtag["text"] not in hashtags:
                    hashtags[hashtag["text"]] = 1

    df = pd.DataFrame.from_dict(hashtags, orient="index")
    df = df.sort_values(by=0, ascending=False)
    df = df.reset_index()
    df.columns = ["hashtag", "count"]

    c = 0
    i = 0

    while c < 10:
        try:
            print(df["hashtag"][i], df["count"][i])
            i += 1
            c += 1
        except UnicodeEncodeError:
            print("UnicodeEncodeError: Could not print hashtag; text not",
                  "supported by Windows/OS/prompt. Skipping hashtag.")
            i += 1


if __name__ == '__main__':
    main()
