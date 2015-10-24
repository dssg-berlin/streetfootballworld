import spacy.en
from spacy.parts_of_speech import NOUN
from collections import defaultdict

dataDir = "/Users/hendster/streetfootballworld/DSSG_unleashfootball/TheRevisedTranslatedPosts"
text = open(dataDir + "/all_posts_concatenated.txt", encoding="ISO-8859-2").read().lower().

nlp = spacy.en.English()
tokens = nlp(text, tag=True, parse=False)
noun_freq = defaultdict(int)
for token in tokens:
    if token.pos == NOUN:
        noun_freq[token.lemma_] += 1
print(noun_freq)

sorted(noun_freq.items(), key= lambda x: x[1], reverse=True)