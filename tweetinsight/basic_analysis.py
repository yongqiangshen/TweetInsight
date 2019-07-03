import nltk
from collections import Counter
import os, sys
from importlib import reload

#reload(sys)
#sys.setdefaultencoding('utf-8')

# remove trivial words
import string

# trivial words to filtered
stopwords_set = set(nltk.corpus.stopwords.words('english'))
stopwords_set.remove(u'again')

nums_set = set([])
for digit in string.digits:
    nums_set.add(digit)
for digit1 in string.digits:
    for digit2 in string.digits:
        dd = digit1 + digit2
        nums_set.add(dd)

extrawords_set = set(
    [u'-', u'.', u'..', u'...', u'--', u'\'',
     u'https', u'p.m', u'a.m', u'000',
     u'co', u'ohio', u'carolina', u'florida', u'colorado', u'iowa', u'alabama', u'hampshire', u'michigan', u'virginia',
     u'wisconsin', u'arizona', u'california', u'indiana', u'texas', u'washington', u'nevada',
     u'charlottesville', u'cleveland', u'pennsylvania', u'phoenix', u'bedminster', u'gettysburg', u'u'])

filter_set = stopwords_set | extrawords_set | nums_set

# substitutes (only deal with 'word for word')
subsList = {'dems': 'democrates', 'ocare': 'healthcare', 'obamacare': 'healthcare', 'hcare': 'healthcare',
            'tpp': 'agreement', 'wikileakes': 'leak', 'brexit': 'exit', 'wwi': 'war', 'wwii': 'war', 'nafta': 'agreement',
            'hrc': 'hillary', 'hillarys': 'hillary', 'hillaryclinton': 'hillary',
            'djt': 'trump', 'melania': 'trump', 'ivanka': 'trump', 'kushner': 'trump', 'donaldtrump': 'trump',
            'dnc': 'democrates', 'usss': 'fbi', 'comey': 'fbi', 'doj': 'justice', 'nypd': 'police',
            'crimea': 'ukraine', 'syrians': 'syrian',
            'buzzfeed': 'media', 'foxconn': 'media', 'breitbart': 'media', 'instagram': 'media', 'amazonwashingtonpost': 'media', 'softbank': 'bank',
            'deplorables': 'humble', 'cancelled': 'cancel', 'cancelling': 'cancel', 'judgement': 'judge', 'americanism': 'american'}
typoList = {'hereos': 'heroes', 'falwell': 'farewell', 'substantialy': 'substantially', 'amercan': 'american'}
subsList.update(typoList)
                
                
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


def wordFilter(wordList, filterWords):
    return [word for word in wordList if word not in filterWords]


def basic_analysis(normalWordbag, capitalWordbag, showWordCloud):
    # filter the stopwords
    normalWordbag = wordFilter(normalWordbag, filter_set)
    capitalWordbag = wordFilter(capitalWordbag, filter_set)

    print('%d non-stop words totally.' % len(normalWordbag))

    # count the word occurrence
    normalCounter = Counter(normalWordbag)
    print('%d non-repeative words.' % len(normalCounter))
    print("Most 30 common words:")
    print(normalCounter.most_common(30))

    #print "ALL CAPITAL:"
    capitalCounter = Counter(capitalWordbag)
    #print capitalCounter.most_common(200)

    # plot the word clouds
    if showWordCloud:
        from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
        import matplotlib
        matplotlib.use("TkAgg")
        import matplotlib.pyplot as plt
        from scipy.misc import imread

        def wordlist2string(wordlist):
            s = ''
            for word in wordlist:
                s += word + ' '
            return s

        normalStringAll = wordlist2string(normalWordbag)
        capitalStringAll = wordlist2string(capitalWordbag).upper()

        # read the mask / color image
        d = os.path.dirname(__file__)
        trump_coloring = imread(os.path.join(d, "static", "trump4.png"))

        wc = WordCloud(background_color="white", mask=trump_coloring, stopwords=STOPWORDS, random_state=1)

        # create coloring from image
        image_colors = ImageColorGenerator(trump_coloring)

        plt.figure(0)

        wordcloud = wc.generate(normalStringAll)
        plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
        #plt.imshow(trump_coloring, cmap=plt.cm.gray)
        plt.axis('off')

        #plt.figure(1)
        #wordcloud = wc.generate(capitalStringAll)
        #plt.imshow(wordcloud.recolor(color_func=image_colors), interpolation='bilinear')
        #plt.axis('off')

        #plt.show()

        # save img
        wc.to_file(os.path.join(d, "static", "cloudimg.png"))

    return

