import spacy
from schedule import schedule_events

# Load the SpaCy English model
nlp = spacy.load("en_core_web_sm")


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
event = []
input_text = "There will be a meeting tomorrow from 9 AM to 11 AM."
event_data = transform_text_to_event_schema(input_text)
print(type(event_data))
event = event + [event_data]
my_schedule = schedule_events(event)
print(my_schedule)