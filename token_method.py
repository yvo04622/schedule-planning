import spacy
from schedule import schedule_events
import json
from spacy.tokens import Span

# Load the SpaCy English model
# nlp = spacy.load("en_core_web_sm")

# Load and preprocess the JSON dataset
# dataset_path = "title.json"
# with open(dataset_path, "r") as f:
#     dataset = json.load(f)

# Prepare the training data
# train_data = []
# for item in dataset:
#     event_description = item["event_description"]
#     event_title = item["event_title"]
#     train_data.append((event_description, event_title))


def transform_text_to_event_schema(input_text):
    # Tokenize the input text and apply POS tagging
    doc = nlp(input_text)

    # Extract relevant information from POS tagging results
    event_title = None
    start_time = None
    end_time = None

    for token in doc:
        if token.pos_ == "NOUN":
            event_title = token.text
        elif token.pos_ == "NUM" and token.dep_ == "nummod":
            if not start_time:
                start_time = int(token.text)
            else:
                end_time = int(token.text)

    # Map extracted information to the event schema format
    event_schema = {
        "title": event_title,
        "start_time": start_time,
        "end_time": end_time,
    }

    return event_schema


# Example usage
if __name__ == "__main__":
    event = []
    input_text = "There will be a meeting tomorrow from 9 AM to 11 AM."

    # for str in input_text:
    #     event_data = transform_text_to_event_schema(str)
    #     print(type(event_data))
    #     event = event + [event_data]
    # my_schedule = schedule_events(event)
    # print(my_schedule)
    nlp = spacy.load('custom_ner_model')
    doc = nlp(input_text)
    entities = [(ent.text, ent.label_) for ent in doc.ents]
    print(entities)
