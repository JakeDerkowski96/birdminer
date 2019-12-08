""" import modules """
import os, sys, subprocess, errno
from time import sleep
import pandas as pd
from pandas.io import sql
import sqlite3 as lite
import csv, re
import twint


''' global variables '''
# twint variable and initialize
c = twint.Config()
c.Hide_output = True
# variables used in gathering data
shsu_gps = "30.714279,-95.547366,3km"
spring_start = '2019-01-16'
spring_end = '2019-05-11'
# storage variables
dirName = "shsuSpring_2019study"
# dirName = "case-test"

rawDBfile = "birdminer.db"
info = 'case_study_report.txt'
words = ["drink", "drunk", "hungover", "hangover", "wasted",\
              "beer", "party", "bar", "club", "weed", "high", \
              "smoke", "stoned", "blazed"]
# file imported as a list of stings
user_list = "user_list.csv"
tweet_list = 'tweet_list.csv'
# export the frequency of user's posts
num_tweets = "tweet_frequency.csv"


# import as variable
def tweet_ListData(tweet_list):
    with open(tweet_list) as f:
        tweets = f.readlines()
        # change [1:] to [:] if there is no header in csv file
    tweets = [x.strip() for x in tweets[:]]

    return tweets


def diction(words):
    d = dict()
    for value in words:
        if value not in d:
            d[value] = 1
        else:
            d[value] += 1

    return d

def count_words(dic):
    for c in dic:
        print(c + ':appears', dic[c], 'times')


count_words(diction(words))

#
# def main():
#     tweets = tweet_ListData(tweet_list)
#     tweets = tweets[:300]
#     count = 0
#
#
#
#     # matching = [s for s in tweets if any(xs in s for xs in words)]
#
#     # word_search(words, tweets)
#
#     # for word in words:
#     #     res = [x for x in tweets if word in x]
#     #     result = open("result.txt", "w")
#     #     result.writelines(res)
#     #     result.close()
#
#
#
#     # for tweet in tweets:
#     #     for word in words:
#     #         if word in tweet:
#     #             count += 1
#     #             print(f"{word}: appeared {count} times.")
#     # print(tweets)
#     # word_search(words, tweets)
#
# main()
