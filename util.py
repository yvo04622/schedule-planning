import spacy
from datetime import datetime


def text_to_timestamp(text):
    try:
        # Attempt to parse the text as a time in 12-hour format with minutes
        time_obj = datetime.strptime(text, "%I:%M %p")
        return time_obj.strftime("%H:%M")
    except ValueError:
        try:
            # Attempt to parse the text as a time in 24-hour format
            time_obj = datetime.strptime(text, "%H")
            return time_obj.strftime("%H:%M")
        except ValueError:
            try:
                # Attempt to parse the text as a time in 12-hour format with minutes
                time_obj = datetime.strptime(text, "%H:%M")
                return time_obj.strftime("%H:%M")
            except ValueError:
                return "Invalid format"


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

# # Example usage
# print(text_to_timestamp("9"))  # Output: 09:00
# print(text_to_timestamp("9:30"))  # Output: 09:30
# print(text_to_timestamp("23"))  # Output: 23:00
# print(text_to_timestamp("12:45 PM"))  # Output: 12:45
