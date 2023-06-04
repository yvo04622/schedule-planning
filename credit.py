def calculate_accuracy(predictions, labels):
    name_total_score = 0
    time_total_score = 0
    data_length = len(labels)

    for i in range(data_length):
        prediction = predictions[i].strip().lower()
        label = labels[i].strip().lower()
        start_time_pred, end_time_pred = prediction.split(",")[1], prediction.split(",")[2]
        start_time_label, end_time_label = label.split(",")[1], label.split(",")[2]

        # calculate name's grade
        if prediction == label:
            name_total_score += 1
        elif prediction in label:
            name_total_score += 0.5

        # calculate time interval's grade
        if start_time_pred == start_time_label and end_time_pred == end_time_label:
            time_total_score += 1

    name_accuracy = (name_total_score / data_length) * 100
    time_accuracy = (time_total_score / data_length) * 100

    return name_accuracy, time_accuracy


input_file1 = 'test/expect.txt'
input_file2 = 'test/output.txt'
labels = []
predictions = []

with open(input_file1, 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        labels.append(line)

with open(input_file2, 'r') as file:
    for line in file:
        parts = line.strip().split(',')
        predictions.append(line)

name_accuracy, time_accuracy = calculate_accuracy(predictions, labels)

print("event name accuracy: {:.2f}%".format(name_accuracy))
print("time interval accuracy: {:.2f}%".format(time_accuracy))