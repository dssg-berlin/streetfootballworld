import spacy.en
from spacy.parts_of_speech import NOUN
from collections import defaultdict

dataDir = "/Users/hendster/streetfootballworld/DSSG_unleashfootball/TheTranslatedPosts"
text = open(dataDir + "/trans_post1.txt").read()
print(text)

nlp = spacy.en.English()
tokens = nlp(text, tag=True, parse=False)
noun_freq = defaultdict(int)
for token in tokens:
    if token.pos == NOUN:
        noun_freq[token.string] += 1
print(noun_freq)

