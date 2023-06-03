import pandas as pd
from tqdm import tqdm
import spacy
from spacy.tokens import DocBin

nlp = spacy.blank("en")  # Load a new spacy model
db = DocBin()  # Create a DocBin object

# with open('data/train_data.txt') as f:
#     lines = f.readlines()

# print(lines)
train_data = [
    [
        "I need to finish the task in 6 hours.\r", {
            "entities": [[21, 25, "EVENT_TITLE"], [29, 30, "DURATION"]]
        }
    ],
    [
        "I have a meeting from 9:00 to 15:00.\r", {
            "entities": [[9, 16, "EVENT_TITLE"], [22, 26, "START_TIME"], [30, 35, "END_TIME"]]
        }
    ],
    [
        "I went to sleep at 23:30.\r", {
            "entities": [[10, 15, "EVENT_TITLE"], [19, 24, "START_TIME"]]
        }
    ],
    ["I take a shower at 21:20.\r", {
        "entities": [[9, 15, "EVENT_TITLE"], [19, 24, "START_TIME"]]
    }],
    [
        "I buy these Frozen Trader Joe's meals at 18:40.\r", {
            "entities": [[32, 37, "EVENT_TITLE"], [41, 46, "START_TIME"]]
        }
    ],
    [
        "I have to get done for finals before 23:59.\r", {
            "entities": [[23, 29, "EVENT_TITLE"], [37, 42, "END_TIME"]]
        }
    ],
    [
        "I also went shopping at SHIRO at 14:49.\r", {
            "entities": [[12, 20, "EVENT_TITLE"], [33, 38, "START_TIME"]]
        }
    ],
    [
        "I see the movie at 19:00.\r", {
            "entities": [[10, 15, "EVENT_TITLE"], [19, 24, "START_TIME"]]
        }
    ],
    [
        "I buy yuzu tea at Kaldi at 10:00.\r", {
            "entities": [[2, 14, "EVENT_TITLE"], [27, 32, "START_TIME"]]
        }
    ],
    ["I'll make lunch at 10:30.\r", {
        "entities": [[5, 15, "EVENT_TITLE"], [19, 24, "START_TIME"]]
    }],
    [
        "I'll do my best to study from 12:00.\r", {
            "entities": [[19, 24, "EVENT_TITLE"], [30, 35, "START_TIME"]]
        }
    ],
    [
        "I'm going to exercise from 13:00 to 14:00.\r", {
            "entities": [[13, 21, "EVENT_TITLE"], [27, 32, "START_TIME"], [36, 41, "END_TIME"]]
        }
    ],
    ["I took a bath at 17:30.\r",
     {
         "entities": [[9, 13, "EVENT_TITLE"], [17, 22, "START_TIME"]]
     }],
    ["I drink coffee at 6:00.\r", {
        "entities": [[2, 14, "EVENT_TITLE"], [18, 22, "START_TIME"]]
    }],
    [
        "I need to go to see a dentist at 15:00.\r", {
            "entities": [[16, 29, "EVENT_TITLE"], [33, 38, "START_TIME"]]
        }
    ],
    [
        "He will go to the amusement park from 10:00 to 17:00 next Sunday.\r", {
            "entities": [[18, 32, "EVENT_TITLE"], [38, 43, "START_TIME"], [47, 52, "END_TIME"]]
        }
    ],
    [
        "I will go hiking from 15:00 to 17:00.\r", {
            "entities": [[10, 16, "EVENT_TITLE"], [22, 27, "START_TIME"], [31, 36, "END_TIME"]]
        }
    ],
    [
        "She will go to the bookstore from 19:00 to 21:00.\r", {
            "entities": [[19, 28, "EVENT_TITLE"], [34, 39, "START_TIME"], [43, 48, "END_TIME"]]
        }
    ],
    [
        "They will go to Big-City from 14:00 to 17:00.\r", {
            "entities": [[16, 24, "EVENT_TITLE"], [30, 35, "START_TIME"], [39, 44, "END_TIME"]]
        }
    ],
    [
        "They have to take THSR at 14:47.\r", {
            "entities": [[18, 22, "EVENT_TITLE"], [26, 31, "END_TIME"]]
        }
    ],
    [
        "They will go to the KTV from 17:00 to 22:00.\r", {
            "entities": [[20, 23, "EVENT_TITLE"], [29, 34, "START_TIME"], [38, 43, "END_TIME"]]
        }
    ], ["", {
        "entities": []
    }]
]

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

db.to_disk("dev.spacy")  # save the docbin object
