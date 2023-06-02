import spacy
from spacy.training import Example
from numpy import random
from collections import defaultdict


# load data
def load_data(file_path):
    data = []
    with open(file_path, 'r') as file:
        for line in file:
            line = line.strip()
            parts = line.split('\t')
            sentence = parts[0]
            print(line, parts, sentence, '\n')
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
train_data = load_data('data/train_data.txt')  # Your annotated training data

# doc = nlp("I have a meeting from 2 PM to 4 PM.")
# entities = [(ent.text, ent.label_) for ent in doc.ents]
# print(entities)

# Convert the training data into spaCy's training format
print('finish\n')
train_examples = []
for sentence, annotations in train_data:
    entities = []
    for start, end, label in annotations:
        entities.append((start, end, label))
    train_examples.append(Example.from_dict(nlp.make_doc(sentence), {"entities": entities}))

# Train the NER component
optimizer = nlp.initialize()
for i in range(10):  # Number of training iterations
    # Shuffle the training
    print('training', i, '\n')
    random.shuffle(train_examples)
    losses = {}
    for example in train_examples:
        nlp.update([example], sgd=optimizer, losses=losses)

# Evaluate the trained model
evaluation_data = load_data('data/eval_data.txt')  # Your evaluation dataset

# Convert the evaluation data into spaCy's Doc objects
eval_docs = [nlp.make_doc(sentence) for sentence, _ in evaluation_data]

# Create dictionaries to store true positives, false positives, and false negatives
true_positives = defaultdict(int)
false_positives = defaultdict(int)
false_negatives = defaultdict(int)

# Run the trained model on the evaluation data
for doc, (_, annotations) in zip(eval_docs, evaluation_data):
    doc = nlp(doc.text)
    # Extract the predicted entities from the doc
    predicted_entities = [(ent.text, ent.label_) for ent in doc.ents]
    # Compare the predicted entities with the gold annotations to calculate metrics
    for gold_entity in annotations:
        if gold_entity in predicted_entities:
            true_positives[gold_entity[2]] += 1
            predicted_entities.remove(gold_entity)
        else:
            false_negatives[gold_entity[2]] += 1

    # Any remaining predicted entities are false positives
    for predicted_entity in predicted_entities:
        false_positives[predicted_entity[1]] += 1

# Calculate precision, recall, and F1-score for each entity label
for label in true_positives:
    tp = true_positives[label]
    fp = false_positives[label]
    fn = false_negatives[label]

    precision = tp / (tp + fp) if (tp + fp) > 0 else 0.0
    recall = tp / (tp + fn) if (tp + fn) > 0 else 0.0
    f1_score = (2 * precision * recall) / (precision + recall) if (precision + recall) > 0 else 0.0

    print(f"Entity: {label}")
    print(f"Precision: {precision}")
    print(f"Recall: {recall}")
    print(f"F1-score: {f1_score}")

# Save the trained model for future use
nlp.to_disk("custom_ner_model")
