from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import cPickle
from time import time
import pandas as pd
from scipy import zeros
import pdb
import json

def load_sentiment(fn='SentiWordNet_3.0.0_20130122.txt'):
    words = dict()
    for line in pd.read_csv(fn,sep='\t',header=26).iterrows():
        for terms in line[1]['SynsetTerms'].split(' '):
            polarity = line[1]['PosScore'] - line[1]['NegScore']
            if abs(polarity) > 0.0:
                words[terms[:-2]] = polarity
    return words

def get_sentiments(data,vectorizer,sentimentDict):
    # bring sentiment words in bag-of-word space
    sentivec = zeros(len(vectorizer.vocabulary_))
    for word in sentimentDict.keys():
        if vectorizer.vocabulary_.has_key(word):
            sentivec[vectorizer.vocabulary_[word]] = sentimentDict[word]
    
    # project data into sentiment-subspace
    return data.dot(sentivec)

def run():
    '''
    Standard topic analysis copied from scikit learn example on 
    http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf.html
    '''
    
    t0 = time()
    n_topics = 100
    n_top_posts = 5
    n_top_words = 10
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, ngram_range=(1,3))

    dataFname = '../DSSG_unleashfootball/word_splits_stopwords'
    originalTexts = '../DSSG_unleashfootball/Original_posts'
    dat = cPickle.load(open(dataFname))
    orig = cPickle.load(open(originalTexts))

    tfidf = vectorizer.fit_transform([' '.join(x) for x in dat])
    nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
    print("done in %0.3fs." % (time() - t0))

    feature_names = vectorizer.get_feature_names()
    
    sentimentWords = json.loads(open('sentiWords.json').read())#load_sentiment()
    sentimentTopics = get_sentiments(nmf.components_,vectorizer,sentimentWords)    

    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topicDict = {}
        topicDict['sentiment'] = sentimentTopics[topic_idx]
        topicDict['keywords'] = [{'keyword':feature_names[i],'weight':nmf.components_[topic_idx,i]} for i in topic.argsort()[:-n_top_words - 2:-1]]
        
        # get some representative posts
        ranking = tfidf.dot(nmf.components_[topic_idx,:]).argsort()[:-n_top_posts][::-1]
        topicDict['posts'] = [{'post':orig[i]} for i in ranking]
        
        #  
        print("Topic #%d (Sentiment %f):" %(topic_idx,sentimentTopics[topic_idx]))
        print(" | ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        open('topic-%d.json'%topic_idx,'wb').write(json.dumps(topicDict))
