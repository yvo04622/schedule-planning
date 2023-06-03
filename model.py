import spacy

nlp = spacy.load('output/model-best')
doc = nlp('I have to finish my homwork from 9 to 11')

print(doc.ents)
