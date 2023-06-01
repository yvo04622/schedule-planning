import spacy
from spacy.training import Example
from numpy import random


# load data
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            parts = line.split('\t')
            sentence = parts[0]
            annotations = [tuple(map(int, entity.split(','))) for entity in parts[1:]]
            data.append((sentence, annotations))
    return data


# Load the pre-trained English model
nlp = spacy.load("en_core_web_sm")

# Add your custom entity labels to the NER component
ner = nlp.get_pipe("ner")
ner.add_label("START_TIME")
ner.add_label("DEADLINE")
ner.add_label("DURATION")
ner.add_label("EVENT_TITLE")

# Prepare and annotate your training data
train_data = load_data('train_data.txt')  # Your annotated training data

# doc = nlp("I have a meeting from 2 PM to 4 PM.")
# entities = [(ent.text, ent.label_) for ent in doc.ents]
# print(entities)

# Convert the training data into spaCy's training format
train_examples = []
for sentence, annotations in train_data:
    entities = []
    for start, end, label in annotations:
        entities.append((start, end, label))
    train_examples.append(Example.from_dict(nlp.make_doc(sentence), {"entities": entities}))

# Train the NER component
optimizer = nlp.initialize()
for _ in range(10):  # Number of training iterations
    # Shuffle the training examples
    random.shuffle(train_examples)
    losses = {}
    for example in train_examples:
        nlp.update([example], sgd=optimizer, losses=losses)

# Evaluate the trained model
evaluation_data = load_data('eval_data.txt')  # Your evaluation dataset

# Convert the evaluation data into spaCy's Doc objects
eval_docs = [nlp.make_doc(sentence) for sentence, _ in evaluation_data]

# Run the trained model on the evaluation data
for doc, (_, annotations) in zip(eval_docs, evaluation_data):
    doc = nlp(doc.text)
    # Extract the predicted entities from the doc
    predicted_entities = [(ent.text, ent.label_) for ent in doc.ents]
    # Compare the predicted entities with the gold annotations to calculate metrics

# Save the trained model for future use
nlp.to_disk("custom_ner_model")
