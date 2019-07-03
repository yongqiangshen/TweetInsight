from flask import render_template
from flask import url_for
from tweetinsight import app
#from sqlalchemy import create_engine
#from sqlalchemy_utils import database_exists, create_database
from flask import request
import pandas as pd
#import psycopg2
#from tweetinsight.a_Model import ModelIt
#from tweetinsight.most_similar import most_similar
from tweetinsight.basic_analysis import *
from tweetinsight.tweet_obj import tweet_obj
from gensim.models import Word2Vec

# Python code to connect to Postgres
# You may need to modify this based on your OS, 
# as detailed in the postgres dev setup materials.

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
'''

tweets_pd = pd.read_csv('data/realDonaldTrump_tweets.csv')

nTweets_full = len(tweets_pd)

nTweets = len(tweets_pd)

'''
# query:
sql_query_analyzed = """
SELECT * FROM trump_tweets_analyzed_table;
"""
tweets_analyzed_pd = pd.read_sql_query(sql_query_analyzed,con)
'''
tweets_analyzed_pd = pd.read_csv('data/realDonaldTrump_tweets_analyzed.csv')


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

# Topic keywords
myTopics = list()
# Topic 1
myTopics.append(['tax', 'cuts', 'vote', 'republicans', 'democrats', 'senate', 'bill', 'big'])
# Topic 2
myTopics.append(['fake', 'news', 'dishonest', 'media', 'failing', 'cnn', 'story', 'corrupt'])
# Topic 3
myTopics.append(['trade', 'china', 'deal', 'tariffs', 'farmers', 'mexico', 'canada', 'billion'])
# Topic 4
myTopics.append(['border', 'wall', 'security', 'immigration', 'democrats', 'southern', 'mexico', 'illegal'])
# Topic 5
myTopics.append(['collusion', 'witch', 'hunt', 'fbi', 'russia', 'hillary', 'crooked', 'report'])
# Topic 6
myTopics.append(['jobs', 'economy', 'market', 'record', 'high', 'unemployment', 'numbers', 'year'])
# Topic 7
myTopics.append(['great', 'state', 'job', 'governor', 'endorsement', 'vote', 'total', 'strong'])
# Topic 8
myTopics.append(['thank', 'happy', 'great', 'american', 'today', 'women', 'honor', 'nation'])
# Topic 9
myTopics.append(['join', 'forward', 'tonight', 'live', 'looking', 'see', 'tomorrow', 'rally'])
# Topic 10
myTopics.append(['make', 'america', 'great', 'again', 'together', 'making', 'safe', 'respected'])
# Topic 11
myTopics.append(['korea', 'north', 'kim', 'un', 'jong', 'nuclear', 'meeting', 'peace'])
# Topic 12
myTopics.append(['honor', 'today', 'welcome', 'prime', 'minister', 'great', 'president', 'leaders'])
# Topic 13
myTopics.append(['god', 'bless', 'united', 'states', 'president', 'donald', 'trump', 'presidential'])
# Topic 14
myTopics.append(['congratulations', 'secretary', 'general', 'white', 'house', 'team', 'attorney', 'great'])
# Topic 15
myTopics.append(['enjoy', 'interviewed', 'tonight', 'working', 'hard', 'morning', 'tomorrow', 'coming'])
# Topic 16
myTopics.append(['rico', 'puerto', 'responders', 'first', 'leaving', 'terrible', 'team', 'side'])

myTopicsNames = ['tax', 'fakeNews', 'trade', 'border', 'fbi', 'jobs', 'vote', 'thank', 'join', 'MAGA', 'korea', 'honor', 'god', 'whitehouse', 'interview', 'ricopuerto']

nMyTopics = len(myTopicsNames)




@app.route('/')
@app.route('/index')
def index():
    return render_template("index.html")

'''
@app.route('/db')
def tweets_page():
    sql_query = """                                                                       
                SELECT * FROM trump_tweets_analyzed_table;          
                """
    query_results = pd.read_sql_query(sql_query,con)
    tweets_text = ""
    for i in range(0,10):
        tweets_text += query_results.iloc[i]['text']
        tweets_text += "<br>"
    return tweets_text 

@app.route('/db_fancy')
def tweets_page_fancy():
    sql_query = """
               SELECT created_y, text, favorite_count FROM trump_tweets_analyzed_table WHERE created_y=2019;
                """
    query_results=pd.read_sql_query(sql_query,con)
    tweets = []
    #for i in range(0,query_results.shape[0]):
    for i in range(0,10):
        tweets.append(dict(created_y=query_results.iloc[i]['created_y'], text=query_results.iloc[i]['text'], favorite_count=query_results.iloc[i]['favorite_count']))
    return render_template('cesareans.html',tweets=tweets)
   

@app.route('/input')
def tweets_input():
    return render_template("input.html")



@app.route('/output')
def tweets_output():
  #pull 'birth_month' from input field and store it
    similar_word = request.args.get('any_word')
    #just select the Cesareans  from the birth dtabase for the month that the user inputs
    query = "SELECT created_y, text, favorite_count FROM trump_tweets_analyzed_table WHERE created_y=2019 AND created_m=3"
    print(query)
    query_results=pd.read_sql_query(query,con)
    print(query_results)
    tweets = []
    for i in range(0,10):
        tweets.append(dict(created_y=query_results.iloc[i]['created_y'], text=query_results.iloc[i]['text'], favorite_count=query_results.iloc[i]['favorite_count']))
        #the_result = ModelIt(tweet_y, tweets)
    the_result = most_similar(similar_word)
    return render_template("output.html", tweets = tweets, the_result = the_result)

    
@app.route('/topic')
def tweets_topic():
    return render_template("lda_N1.html")
    
@app.route('/charts')
def tweets_charts():
    return render_template("charts.html")
    
@app.route('/tables')
def tweets_tables():
    return render_template("tables.html")
'''
    
@app.route('/topic_list')
def tweets_topic_list():
  #pull 'birth_month' from input field and store it
    html_name = request.args.get('twitter_name')
    return render_template("topic_list.html", html_name=html_name)
    
@app.route('/result')
def tweets_result():
    html_name = request.args.get('twitter_name')
    return render_template("result.html", html_name=html_name)
    
@app.route('/word_cloud')
def tweets_word_cloud():
    basic_analysis(normalWordbag, capitalWordbag, True)    
    return render_template("word_cloud.html")

@app.route('/topic_hotness')
def tweets_topic_hotness():
    return render_template("topic_hotness.html")
    
@app.route('/topic_favorite')
def tweets_topic_favorite():
    return render_template("topic_favorite.html")
    
@app.route('/word_search_input')
def tweets_word_search_input():
    return render_template("word_search_input.html")
    
@app.route('/word_search_output')
def tweets_word_search_output():
  #pull 'birth_month' from input field and store it
    similar_word = request.args.get('word_search')
    
    m2vmethod = 1  # methodType: 0: CBOW; 1: skip-gram
    epoch = 40
    nFeatures = 500
    token_texts = [text.split() for text in texts if len(text) > 0]
    w2v_Trump = Word2Vec(token_texts, sg=m2vmethod, iter=40, size=nFeatures, min_count=1, window=5, workers=2)  
    words = w2v_Trump.wv.most_similar(positive=[similar_word])
    return render_template("word_search_output.html", words = words)
    
@app.route('/topic_search_input')
def tweets_topic_search_input():
    return render_template("topic_search_input.html")
    
@app.route('/topic_search_output')
def tweets_topic_search_output():
  #pull 'birth_month' from input field and store it
    twitter_year = int(request.args.get('year'))
    twitter_month = int(request.args.get('month'))
    twitter_topic = int(request.args.get('topic'))
 
    # given a Topic, list the most similar tweets in a specific month
    related_tweets = []
    #related_tweets.append('For Topic [' + myTopicsNames[twitter_topic-1] + ']:')
    tweets_month = tweets_analyzed_pd[(tweets_analyzed_pd['created_y'] == twitter_year) & (tweets_analyzed_pd['created_m'] == twitter_month)]
    text_month = tweets_month['normalText'].values
    simu_month = tweets_month[myTopicsNames[twitter_topic-1]+'_trans'].values
    sorted_simu_month = simu_month.argsort()[:-len(simu_month)-1:-1]
    sorted_text_month = [text_month[i] for i in sorted_simu_month]
    #[str(topic[i]) + '*' + featureNames[i] for i in topic.argsort()[:-n_top_words-1:-1]]

    for i in range(min(15, len(tweets_month))):
        related_tweets.append(dict(date=str(twitter_year)+'-'+str(twitter_month)+'-'+str(tweets_month.iloc[sorted_simu_month[i]]['created_d']), time=str(tweets_month.iloc[sorted_simu_month[i]]['created_h']) + ':' + str(tweets_month.iloc[sorted_simu_month[i]]['created_min']), text=sorted_text_month[i], similarity=simu_month[sorted_simu_month[i]]))
        #related_tweets.append(sorted_text_month[i], simu_month[sorted_simu_month[i]])
        #related_tweets.append(str(twitter_year)+'-'+str(twitter_month)+'-'+str(tweets_month.iloc[sorted_simu_month[i]]['created_d']), str(tweets_month.iloc[sorted_simu_month[i]]['created_h']) + ':' + str(tweets_month.iloc[sorted_simu_month[i]]['created_min']))
 
    return render_template("topic_search_output.html", related_tweets = related_tweets)   
