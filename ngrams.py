from nltk.util import ngrams
from nltk.corpus import stopwords
import nltk

#nltk.download()

data_source_dir = "/home/silviapina/DATA/DSSG_unleashfootball/TheTranslatedPosts/"
prefix="trans_post"

data =[]
for i in range(1,456):
    file_name=data_source_dir+prefix+str(i)+".txt"
    with open(file_name, encoding="ISO-8859-2") as f:
        text=f.read()
        data.append(text)

join_text = " ".join(data)
english_stops= set(stopwords.words("english"))

join_text_without_stops = [word for word in join_text.split(" ") if word not in english_stops]
n = 1
onegrams = ngrams(join_text_without_stops, n)

for grams in onegrams:
    print(grams)



