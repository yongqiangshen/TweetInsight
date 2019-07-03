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
#       print(tweetObj.text)
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

# use only the twitter texts to train a word2vec model
from tweetinsight.basic_analysis import filter_set

m2vmethod = 1  # methodType: 0: CBOW; 1: skip-gram
epoch = 40
nFeatures = 500
token_texts = [text.split() for text in texts if len(text) > 0]
#token_texts = [text for text in texts]
#w2v_Trump = w2v_analyzer.w2v_analyzer(token_texts, m2vmethod, nFeatures, epoch, filter_set)
#w2v_Trump.fit(token_texts)

from gensim.models import Word2Vec

w2v_Trump = Word2Vec(token_texts, sg=m2vmethod, iter=40, size=nFeatures, min_count=1, window=5, workers=2)
#w2v_Trump.wv['vote']

def most_similar(anyWord):
    return w2v_Trump.wv.most_similar(positive=[anyWord])

