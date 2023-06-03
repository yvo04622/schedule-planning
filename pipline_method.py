import pandas as pd
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin
import json

nlp = spacy.blank("en")  # Load a new spacy model
db = DocBin()  # Create a DocBin object

# with open('data/train_data.txt') as f:
#     lines = f.readlines()

# print(lines)
train_data = []  # List to store training data

# # Open and read your text file
# with open('data/train_data.txt', 'r') as file:
#     data = json.load(file)

# # Iterate over the data and create training examples
# for item in data:
#     text = item[0].strip()
#     entities = item[1]['entities']
#     train_data.append((text, {'entities': entities}))

for text, annot in tqdm(train_data):  # data in previous format
    doc = nlp.make_doc(text)  # create doc object from text
    ents = []
    for start, end, label in annot["entities"]:  # add character indexes
        span = doc.char_span(start, end, label=label, alignment_mode="contract")
        if span is None:
            print("Skipping entity")
        else:
            ents.append(span)
    doc.ents = ents  # label the text with the ents
    db.add(doc)

db.to_disk("train.spacy")  # save the docbin object
