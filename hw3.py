import nltk
import wikipedia
import codecs
from nltk.corpus import brown
import scrapy

results = wikipedia.search("Wikipedia")
page = wikipedia.page("Tesco")

text = page.summary.encode('ascii', 'ignore')

## POS Tagging

sentences = nltk.sent_tokenize(text)
tokens = [nltk.word_tokenize(sent) for sent in sentences]
tagged = [nltk.pos_tag(sent) for sent in tokens]

print(tagged)

## entity classification
tokens = nltk.word_tokenize(text)
tagged = nltk.pos_tag(tokens)
ne_chunked = nltk.ne_chunk(tagged, binary=True)

def extractEntities(ne_chunked):
    data = {}
    for entity in ne_chunked:
        if isinstance(entity, nltk.tree.Tree):
            text = " ".join([word for word, tag in entity.leaves()])
            ent = entity.label()
            data[text] = ent
        else:
            continue
    return data


print(extractEntities(ne_chunked))

sentences = nltk.sent_tokenize(text)
tokens = nltk.word_tokenize(sentences[0])
tagged = nltk.pos_tag(tokens)

## custom ner
entity = []
output = ""
for tagged_entry in tagged:
    if (len(entity) == 0 and tagged_entry[1].startswith("JJ") or ( len(entity) > 0 and tagged_entry[1].startswith("NN"))):
        entity.append(tagged_entry)
    else:
        if entity and len(entity) == 3:
            output = " ".join(e[0] for e in entity)
            break
        elif not output and entity and len(entity) == 2:
            output = " ".join(e[0] for e in entity)
        entity = []

print(output)