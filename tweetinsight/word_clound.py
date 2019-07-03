import os, sys
import pandas as pd
from tweetinsight.tweet_obj import tweet_obj
import logging
import pickle
from sqlalchemy import create_engine
from sqlalchemy_utils import database_exists, create_database
import psycopg2

'''
read data
'''
user = 'yongqiangshen' #add your Postgres username here      
host = 'localhost'
dbname = 'tweets_db'
db = create_engine('postgres://%s%s/%s'%(user,host,dbname))
con = None
con = psycopg2.connect(database = dbname, user = user, host = host, password = 'mypassword') #add your Postgres password here


# query:
sql_query = """
SELECT * FROM trump_tweets_table;
"""
tweets_pd = pd.read_sql_query(sql_query,con)


nTweets_full = len(tweets_pd)

nTweets = len(tweets_pd)


'''
analysis
'''
# if we neglect the retweets
ignore_RT = True
ignore_Quote = False
use_hashtag = False

def getTweetNormalTokens(tweetObj):

    normalTokens = list()
    for tokenObj in tweetObj.tokenList:
        if tokenObj.type == 0:
            if not ignore_Quote or not tokenObj.inQuote:
                normalTokens.append(tokenObj.content)
        elif use_hashtag and tokenObj.type == 2:
            normalTokens.append(tokenObj.content)

    return normalTokens

def getTweetCaptialTokens(tweetObj):
    capitalTokens = list()
    for tokenObj in tweetObj.tokenList:
        if tokenObj.isCapital and tokenObj.type == 0 and not tokenObj.inQuote:
            capitalTokens.append(tokenObj.content)
    return capitalTokens

def list2string(tokenList):
    s = ''
    for i, token in enumerate(tokenList):
        s += token
        if i < len(tokenList)-1:
            s += ' '
    return s

# analyze all tweets, get their tokens with their types
normalWordbag = list()
capitalWordbag = list()
clearTextList = list()
normalTokensList = list()
texts = list()
for i in range(nTweets):
    tweetObj = tweet_obj(tweets_pd.iloc[i])
    tweetObj.text_analyzer()

#    if i == 296:
#        print(tweetObj.text)
#        print(tweetObj.convert2analysis())

    if ignore_RT and len(tweetObj.retweet_source) > 0:
        normalTokensList.append('')
        texts.append('')
    else:
        normalTokens = getTweetNormalTokens(tweetObj)
        normalWordbag.extend(normalTokens)

        capitalTokens = getTweetCaptialTokens(tweetObj)
        capitalWordbag.extend(capitalTokens)

        clearTextList.append(tweetObj.getClearText())
        normalTokensList.append(normalTokens)
        texts.append(list2string(normalTokens))


#print('%d tweets, %d words totally.' % (nTweets, len(normalWordbag)))

tweets_pd['normalText'] = texts
tweets_pd['hasText'] = [len(text) > 0 for text in texts]

# basic analysis
from tweetinsight.basic_analysis import *
#basic_analysis(normalWordbag, capitalWordbag, True)
basic_analysis(normalWordbag, capitalWordbag, False)

