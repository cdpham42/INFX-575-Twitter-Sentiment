# -*- coding: utf-8 -*-
"""
Created on Sun Apr  8 13:21:08 2018

@author: Casey
"""

import sys
import json
import csv
import string
import re


def main():

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

    # Lists and dictionaries for states

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

            # Getting location via coordinates not used, as no tweets in my
            # output.txt contain coordinates that are within the US. Thus
            # skipped to remove unneeded code.
            #
            # Additionally, reverse geolocation requires external library
            # reverse_geocoder, another reason this is not included.s

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

    print(max(happy_states, key=happy_states.get))


if __name__ == '__main__':
    main()
