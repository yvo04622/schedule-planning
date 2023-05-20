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
input_text = "There will be a meeting tomorrow from 9 AM to 11 AM."
event_data = transform_text_to_event_schema(input_text)

if event_data["start_time"] is not None and event_data["end_time"] is not None:
    events = [event_data]
    scheduled_events = schedule_events(events)
    for event in scheduled_events:
        print(event)
else:
    print("Invalid input. Start time or end time not provided.")
my_schedule = schedule_events(event_data)
print(my_schedule)