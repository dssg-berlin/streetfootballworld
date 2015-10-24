
# coding: utf-8

# In[11]:

import spacy.en
from spacy.parts_of_speech import NOUN
from collections import defaultdict


# In[12]:

dataDir = "/Users/hendster/streetfootballworld/DSSG_unleashfootball/TheTranslatedPosts"
text = open(dataDir + "/trans_post1.txt").read()
print(text)


# In[15]:

nlp = spacy.en.English()
tokens = nlp(text, tag=True, parse=False)
noun_freq = defaultdict(int)
for token in tokens:
    if token.pos == NOUN:
        noun_freq[token.string] += 1
print(noun_freq)


# In[ ]:



