# -*- coding: utf-8 -*-
"""
Created on Mon Apr  2 13:45:19 2018

@author: Casey

INFX 475 Assignment 01 - Twitter Sentiment Analysis
"""

# %%

import sys
import os
import json
import csv
import string
import re
import pandas as pd

path = "D:\Google Drive\cdpham42\Classes\INFX 575 Data Science 3 "\
        "Scaling Applications and Ethics\Assignments\Assignment 01 "\
        "- Twitter Sentiment Analysis"
sys.path.append(path)
print(sys.path)
os.chdir(path)

# %%

sentiments = {}
tweets = []

with open("AFINN-111.txt") as f:
    for line in csv.reader(f, delimiter="\t"):
        sentiments[line[0]] = int(line[1])

with open("output.txt") as f:
    for line in f:
        tweets.append(json.loads(line))

# Set regex for removing punctuation
regex = re.compile('[%s]' % re.escape(string.punctuation))

# %%

tweet_sent = []

c = 1

for tweet in tweets:

    if "text" in tweet:
        this_sent = 0

        text = tweet["text"]
        text = regex.sub("", text)
        text = text.lower()

        if c == 1:
            print(text)
            c += 1

        for word in text.split(" "):
            if word in sentiments:
                this_sent += sentiments[word]

        tweet_sent.append(this_sent)

    else:
        tweet_sent.append(0)
        continue

# %%

word_sent = {}

for tweet in tweets:

    if "text" in tweet:
        # Restrict to English, due to output encoding errors
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
                # Set to 1/1 so neutral sentiment is 1; posive > 1, negative < 1
                # in final calculation os sentiment scores
                if word not in sentiments:
                    if word not in word_sent:
                        word_sent[word] = [1, 1]
                    # Adjust word sentiment score:
                    if word in word_sent:
                        # Positive Sentiment
                        if this_sent > 0:
                            word_sent[word][0] += 1
                        # Negative Sentiment
                        elif this_sent < 0:
                            word_sent[word][1] += 1

for word in word_sent:
    word_sent[word] = word_sent[word][0]/word_sent[word][1]

# Write to file for inspection
with open("term_sentiment.txt", "w+") as f:
    for word in word_sent:
        f.write("%s    %f\n"%(word, word_sent[word]))

# Print tweet sentiments, each element on a new line
for word in word_sent:
    print(word, word_sent[word])

# %%


states_abb = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
              "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
              "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
              "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
              "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

states = ['Alabama', 'Alaska', 'Arizona', 'Arkansas', 'California', 'Colorado',
          'Connecticut', 'Delaware', 'Florida', 'Georgia', 'Hawaii', 'Idaho',
          'Illinois', 'Indiana', 'Iowa', 'Kansas', 'Kentucky', 'Louisiana',
          'Maine', 'Maryland', 'Massachusetts', 'Michigan', 'Minnesota',
          'Mississippi', 'Missouri', 'Montana', 'Nebraska', 'Nevada',
          'New Hampshire', 'New Jersey', 'New Mexico', 'New York',
          'North Carolina', 'North Dakota', 'Ohio',
          'Oklahoma', 'Oregon', 'Pennsylvania', 'Rhode Island',
          'South Carolina', 'South Dakota', 'Tennessee', 'Texas', 'Utah',
          'Vermont', 'Virginia', 'Washington', 'West Virginia',
          'Wisconsin', 'Wyoming']

state_dict = {k: v for (k, v) in zip(states, states_abb)}

happy_states = {k: 0 for k in states_abb}

for tweet in tweets:

    if "text" in tweet:
        this_sent = 0

        text = tweet["text"]
        text = regex.sub("", text)
        text = text.lower()

        for word in text.split(" "):
            if word in sentiments:
                this_sent += sentiments[word]

        # Get location via place attribute of tweet
        if "place" in tweet:
            if tweet["place"] is not None:
                for place in tweet["place"]["full_name"].split(", "):
                    if place in states_abb:
                        happy_states[place] += this_sent
                    elif place in states:
                        happy_states[state_dict[place]] += this_sent

        # Else get location via user location
        elif "user" in tweet:
            if tweet["user"]["location"] is not None:
                for place in tweet["user"]["location"].split(", "):
                    if place in states_abb:
                        happy_states[place] += this_sent
                    elif place in states:
                        happy_states[state_dict[place]] += this_sent

# %%

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

for i in range(10):
    print(df["hashtag"][i], df["count"][i])
