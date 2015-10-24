from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import cPickle
from time import time
import pandas as pd
from scipy import zeros,corrcoef,array,sparse
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
    
    # compute sentiments for each
    if sparse.issparse(data):
        sentiments = [corrcoef(array(data[idx,:].todense()),sentivec)[1,0] for idx in range(data.shape[0])]
    else:
        sentiments = [corrcoef(data[idx,:],sentivec)[1,0] for idx in range(data.shape[0])]
    return array(sentiments)

def run():
    '''
    Standard topic analysis copied from scikit learn example on 
    http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf.html
    '''
    
    t0 = time()
    n_topics = 10
    n_top_posts = 20
    n_top_words = 10
    ngram = 1
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2, ngram_range=(1,ngram))

    dataFname = '../DSSG_unleashfootball/word_splits_stopwords'
    originalTexts = '../DSSG_unleashfootball/Original_posts'
    dat = cPickle.load(open(dataFname))
    orig = cPickle.load(open(originalTexts))

    tfidf = vectorizer.fit_transform([' '.join(x) for x in dat])
    nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
    print("Done fitting NMF in %0.3fs." % (time() - t0))

    topic_assignments = nmf.transform(tfidf).argmax(axis=1)

    feature_names = vectorizer.get_feature_names()
    
    sentimentWords = json.loads(open('sentiWords.json').read())#load_sentiment()
    sentimentTopics = get_sentiments(nmf.components_,vectorizer,sentimentWords)    
    sentiments = get_sentiments(tfidf,vectorizer,sentimentWords)
    topics = []
    for topic_idx, topic in enumerate(nmf.components_):
        topicDict = {}
        topicDict['sentiment'] = sentimentTopics[topic_idx]
        topicDict['keywords'] = [{'keyword':feature_names[i],'weight':nmf.components_[topic_idx,i]} for i in topic.argsort()[:-n_top_words - 2:-1]]
        
        topicDict['label'] = topicDict['keywords'][0]['keyword']

        # count number of posts in this topic
        topicDict['postCount'] = (topic_assignments==topic_idx).sum()

        # get some representative posts
        ranking = tfidf.dot(nmf.components_[topic_idx,:])
        ranks = ranking.argsort()[-n_top_posts:][::-1]
        topicDict['posts'] = []
        for item in ranks:
            topicDict['posts'].append({'post':orig[item],'relevance':ranking[item],'sentiment':sentiments[item]})
        
        print("Topic #%d (Sentiment %f):" %(topic_idx,sentimentTopics[topic_idx]))
        print(" | ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        topics.append(topicDict)    
    
    open('topics.json','wb').write(json.dumps(topics))
