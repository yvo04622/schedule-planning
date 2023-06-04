import spacy
from util import text_to_timestamp
from scheduling_for_one_day import read_events_from_file
from scheduling_for_one_day import schedule_events

input_file = 'test/input.txt'
output_file = 'test/output.txt'
nlp = spacy.load('output/model-best')
# Open the file in read mode
file_path = 'path/to/your/file.txt'
file = open(input_file, 'r')
target = open(output_file, 'w')
# Read the file line by line
for line in file:
    # Process each line
    doc = nlp(line)
    title = ''
    start = text_to_timestamp('0')
    end = text_to_timestamp('23:59')
    # Iterate over the entities in the document
    for entity in doc.ents:
        # Print the entity text and its label
        print(f"Entity: {entity.text}, Label: {entity.label_}")
        if entity.label_ == 'START_TIME':
            start = text_to_timestamp(entity.text)
        elif entity.label_ == 'END_TIME':
            end = text_to_timestamp(entity.text)
        else:
            title = entity.text

    print(f"Title:{title}, Start:{start}, End:{end}")
    # Open the file in write mode

    # Write content to the file
    target.write(f'{title},{start},{end}\n')

# Close the file
target.close()

# Close the file
file.close()

# read data
file_path = 'test/output.txt'
events = read_events_from_file(file_path)

schedule, give_up = schedule_events(events)

# Print the schedule in chronological order.
print("Today's schedule:")
schedule = sorted(schedule, key=lambda event: event['start_time'])
for event in schedule:
    print(f"{event['start_time']} - {event['end_time']} {event['name']}")

print()
print("Give up event:")
for event in give_up:
    print(event)