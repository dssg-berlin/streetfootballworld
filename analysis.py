from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import NMF
import cPickle
from time import time


def run():
'''
Standard topic analysis copied from scikit learn example on 
http://scikit-learn.org/stable/auto_examples/applications/topics_extraction_with_nmf.html
'''
    t0 = time()
    n_topics = 100
    n_top_words = 100
    vectorizer = TfidfVectorizer(max_df=0.95, min_df=2)

    fname = '/Users/felix/Code/Python/streetfootballworld/DSSG_unleashfootball/word_splits_stopwords'
    dat = cPickle.load(open(fname))

    tfidf = vectorizer.fit_transform([' '.join(x) for x in dat])
    nmf = NMF(n_components=n_topics, random_state=1).fit(tfidf)
    print("done in %0.3fs." % (time() - t0))

    feature_names = vectorizer.get_feature_names()

    for topic_idx, topic in enumerate(nmf.components_):
        print("Topic #%d:" % topic_idx)
        print(" ".join([feature_names[i]
                        for i in topic.argsort()[:-n_top_words - 1:-1]]))
        print()
